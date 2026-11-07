"""
Fact Summarization & Issue Identification Module for LexAssist.
Extracts facts, legal questions, and search terms from user queries.
"""

import re
from llm.gemini_client import generate_text, get_gemini_client

def extract_facts_and_issues(user_input: str) -> dict:
    """
    Analyzes raw factual scenario and identifies legal issues.
    Falls back to deterministic extraction if offline.
    """
    if not user_input or not user_input.strip():
        return {
            "summary": "No case facts provided.",
            "issues": [],
            "search_query": ""
        }

    client = get_gemini_client()
    if client:
        prompt = f"""Analyze the following factual scenario for legal research:

CASE FACTS / SCENARIO:
\"\"\"{user_input}\"\"\"

Instructions:
1. Provide a concise 2-sentence factual summary.
2. If the text has no legal relevance or is completely non-legal (e.g. cooking recipe, casual chatter, sports scores), set ISSUES to 'NONE' and SEARCH_QUERY to 'NONE'.
3. Otherwise, list 2-3 potential legal issues (phrase cautiously using terms like 'potential applicability', 'possible breach', 'alleged deficiency') and a clean 5-8 word search query suitable for semantic vector retrieval of Indian statutes.

Format output as:
SUMMARY: <text>
ISSUES:
- <issue 1 or NONE>
SEARCH_QUERY: <search query or NONE>
"""
        response = generate_text(prompt)
        return parse_extraction_response(response, user_input)
    else:
        # Offline / Deterministic Heuristic Fallback
        summary = f"Factual scenario regarding: '{user_input[:120]}...'"
        issues = [
            "Potentially relevant to contractual rights or statutory duties under Indian law",
            "Requires evaluation against indexed statutory provisions and official precedents"
        ]
        search_query = user_input
        return {
            "summary": summary,
            "issues": issues,
            "search_query": search_query
        }

def parse_extraction_response(response_text: str, fallback_query: str) -> dict:
    """Parses formatted Gemini output into clean dictionary."""
    summary_match = re.search(r"SUMMARY:\s*(.*?)(?=\nISSUES:|\nSEARCH_QUERY:|$)", response_text, re.DOTALL)
    issues_match = re.search(r"ISSUES:\s*(.*?)(?=\nSEARCH_QUERY:|$)", response_text, re.DOTALL)
    query_match = re.search(r"SEARCH_QUERY:\s*(.*?)$", response_text, re.DOTALL)

    summary = summary_match.group(1).strip() if summary_match else "Fact summary extracted from user scenario."

    raw_issues = issues_match.group(1).strip() if issues_match else ""
    issues = [i.strip("- *").strip() for i in raw_issues.split("\n") if i.strip()]
    
    raw_query = query_match.group(1).strip() if query_match else fallback_query

    # Non-legal classification
    if "NONE" in [i.upper() for i in issues] or raw_query.upper() == "NONE":
        return {
            "summary": summary,
            "issues": ["No relevant legal issues identified in this non-legal scenario."],
            "search_query": ""
        }

    if not issues:
        issues = ["Possible statutory applicability based on reported facts."]

    return {
        "summary": summary,
        "issues": issues,
        "search_query": raw_query
    }
