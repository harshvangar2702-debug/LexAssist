"""
Core Grounded RAG Analysis Engine for LexAssist.
Enforces the Zero-Hallucination Legal Safety Rule and formats traceable research answers.
"""

from retrieval.search import search_provisions, DEFAULT_DISTANCE_THRESHOLD
from analysis.issue_extraction import extract_facts_and_issues
from llm.gemini_client import generate_text, get_gemini_client

def run_lexassist_analysis(user_query: str, top_k: int = 3, distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD) -> dict:
    """
    Full Grounded RAG Pipeline:
    1. Extract facts and legal issues.
    2. Retrieve top statutory provisions from local ChromaDB.
    3. Apply Zero-Hallucination Safety Rule (refuse if empty/irrelevant).
    4. Generate grounded explanation using Gemini API constrained to retrieved text.
    5. Format structured response with full citation traceability.
    """
    if not user_query or not user_query.strip():
        return {
            "success": False,
            "error": "Please provide a valid research question or case scenario."
        }

    # Step 1: Fact and Issue Extraction
    fact_analysis = extract_facts_and_issues(user_query)
    search_term = fact_analysis["search_query"] or user_query

    # Step 2: ChromaDB Retrieval with raw user query inspection for explicit section requests
    retrieved_provisions = search_provisions(
        query_text=search_term,
        top_k=top_k,
        distance_threshold=distance_threshold,
        raw_user_input=user_query
    )

    # Step 3: CRITICAL LEGAL SAFETY RULE - Anti-Hallucination Guardrail
    if not retrieved_provisions:
        return {
            "success": True,
            "found_provisions": False,
            "case_summary": fact_analysis["summary"],
            "legal_issues": fact_analysis["issues"],
            "retrieved_provisions": [],
            "message": "No sufficiently relevant provision was found in the indexed legal corpus.",
            "why_relevant": "Because no statutory provisions matching the distance threshold were retrieved from the indexed database, no legal reasoning was generated to prevent hallucination.",
            "limitations": (
                "LexAssist currently indexes a limited corpus of 3 Indian enactments (Indian Contract Act 1872, "
                "Information Technology Act 2000, Consumer Protection Act 2019). The requested provision may exist "
                "in another statute or require broader legal indexing."
            ),
            "disclaimer": get_mandatory_disclaimer()
        }

    # Step 4: Grounded Explanation Generation via Gemini
    why_relevant_text = generate_grounded_relevance(
        facts=user_query,
        provisions=retrieved_provisions
    )

    return {
        "success": True,
        "found_provisions": True,
        "case_summary": fact_analysis["summary"],
        "legal_issues": fact_analysis["issues"],
        "retrieved_provisions": retrieved_provisions,
        "why_relevant": why_relevant_text,
        "limitations": (
            "1. LexAssist only searched its indexed legal corpus of 3 official Indian statutes.\n"
            "2. It does not contain the entire Indian statutory framework or judicial case precedents.\n"
            "3. Statutory provisions are subject to legislative amendments and judicial interpretations."
        ),
        "disclaimer": get_mandatory_disclaimer()
    }

def generate_grounded_relevance(facts: str, provisions: list) -> str:
    """
    Prompts Gemini to explain why the retrieved provisions may apply to the facts.
    Strictly constrains the LLM to the provided retrieved provisions ONLY.
    """
    client = get_gemini_client()
    if not client:
        # Offline deterministic reasoning format
        explanation_lines = []
        for p in provisions:
            explanation_lines.append(
                f"• Section {p['section_number']} ({p['section_title']}) of {p['law_name']} may be potentially relevant "
                f"to the reported facts regarding '{facts[:60]}...' because it governs {p['section_title'].lower()}."
            )
        return "\n".join(explanation_lines)

    provisions_formatted = ""
    for p in provisions:
        provisions_formatted += (
            f"LAW: {p['law_name']}\n"
            f"SECTION: {p['section_number']}\n"
            f"TITLE: {p['section_title']}\n"
            f"RETRIEVED TEXT:\n{p['text']}\n\n"
        )

    system_instruction = (
        "You are an AI legal research assistant. You MUST base your explanation ONLY on the user's facts "
        "and the EXACT retrieved statutory provisions provided below. Do NOT use outside general legal knowledge. "
        "Do NOT invent any section number, law name, or legal principle. Use cautious legal language such as "
        "'potentially relevant', 'may apply', 'requires professional verification'."
    )

    prompt = f"""USER FACTS:
\"\"\"{facts}\"\"\"

RETRIEVED OFFICIAL LEGAL PROVISIONS:
\"\"\"{provisions_formatted}\"\"\"

TASK:
Write a concise 2-3 paragraph explanation detailing why each retrieved provision may be relevant to the user's facts.
Constraint: Reference ONLY the provided statutory sections above.
"""

    return generate_text(prompt, system_instruction=system_instruction)

def answer_case_followup(
    user_question: str,
    case_facts: str,
    retrieved_provisions: list,
    chat_history: list = None
) -> dict:
    """
    Answers an interactive follow-up question regarding an already-analyzed case.
    Also checks ChromaDB for any additional provisions relevant to the follow-up question.
    """
    if not user_question or not user_question.strip():
        return {"answer": "Please ask a question about the case.", "new_provisions": []}

    # Step 1: Check if user's follow-up question brings in an additional statutory provision
    new_provisions = []
    additional_matches = search_provisions(
        query_text=user_question,
        top_k=2,
        distance_threshold=DEFAULT_DISTANCE_THRESHOLD,
        raw_user_input=user_question
    )

    existing_ids = {p["document_id"] for p in (retrieved_provisions or [])}
    for match in additional_matches:
        if match["document_id"] not in existing_ids:
            new_provisions.append(match)

    combined_provisions = list(retrieved_provisions or []) + new_provisions

    client = get_gemini_client()
    if not client:
        # Offline fallback
        if combined_provisions:
            sec_refs = ", ".join([f"Section {p['section_number']} of {p['law_name']}" for p in combined_provisions])
            answer = (
                f"Regarding your question '{user_question}':\n\n"
                f"Based on the analyzed case facts and the retrieved provisions ({sec_refs}), "
                f"this issue requires evaluation under the statutory conditions specified in the official sections above.\n\n"
                f"(Note: To get live dynamic answers, configure your valid GEMINI_API_KEY in the .env file)."
            )
        else:
            answer = (
                "No sufficiently relevant provision was found in the indexed legal corpus for this question. "
                "LexAssist only answers based on verified official texts in its database."
            )
        return {"answer": answer, "new_provisions": new_provisions}

    # Step 2: Format provisions and conversation history
    provisions_formatted = ""
    for p in combined_provisions:
        provisions_formatted += (
            f"LAW: {p['law_name']}\n"
            f"SECTION: {p['section_number']}\n"
            f"TITLE: {p['section_title']}\n"
            f"RETRIEVED TEXT:\n{p['text']}\n\n"
        )

    history_formatted = ""
    if chat_history:
        for turn in chat_history[-6:]:
            role = "User" if turn.get("role") == "user" else "Assistant"
            history_formatted += f"{role}: {turn.get('content')}\n"

    system_instruction = (
        "You are LexAssist, an AI legal research assistant. You are conversing with a user about a specific case.\n"
        "STRICT LEGAL SAFETY RULES:\n"
        "1. Base your answer strictly on the case facts and the official retrieved provisions provided below.\n"
        "2. NEVER invent section numbers, article numbers, or statutory laws.\n"
        "3. If the user asks about an issue not covered by the retrieved legal provisions or outside Indian Contract Act, "
        "IT Act, or Consumer Protection Act, explicitly state: 'This matter is not covered in the currently indexed legal corpus.'\n"
        "4. Use cautious language ('may apply', 'requires professional verification').\n"
        "5. Do NOT provide legal advice."
    )

    prompt = f"""ORIGINAL CASE FACTS:
\"\"\"{case_facts}\"\"\"

OFFICIAL RETRIEVED STATUTORY PROVISIONS:
\"\"\"{provisions_formatted}\"\"\"

RECENT CONVERSATION HISTORY:
\"\"\"{history_formatted}\"\"\"

USER'S FOLLOW-UP QUESTION:
\"{user_question}\"

Provide a direct, helpful, grounded answer addressing the user's question.
"""

    answer_text = generate_text(prompt, system_instruction=system_instruction)
    return {
        "answer": answer_text,
        "new_provisions": new_provisions
    }

def get_mandatory_disclaimer() -> str:
    return (
        "LexAssist is an AI-assisted legal research tool and does not provide legal advice. "
        "The retrieved provisions, legal issues, and generated explanations should be independently "
        "verified against current official sources by a qualified legal professional before being relied upon."
    )

if __name__ == "__main__":
    sample_query = "A vendor failed to deliver goods after receiving payment."
    res = run_lexassist_analysis(sample_query)
    print("LexAssist Analysis Output:")
    print(f"Summary: {res['case_summary']}")
    print(f"Provisions Found: {res['found_provisions']} ({len(res['retrieved_provisions'])} sections)")
    print(f"Why Relevant:\n{res['why_relevant']}")
