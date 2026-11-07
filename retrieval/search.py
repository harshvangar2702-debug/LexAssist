"""
Semantic Retrieval Module for LexAssist.
Queries ChromaDB for statutory provisions relevant to a legal scenario.
Enforces relevance distance thresholding and explicit section number verification.
"""

import os
import re
import chromadb

CHROMA_DB_DIR = os.path.join(".", "chroma_db")
COLLECTION_NAME = "lexassist_provisions"

# Cosine distance threshold (smaller = more similar).
# Distance <= 0.52 represents tight, genuine semantic legal relevance.
# Distances > 0.52 capture generic preamble or unindexed noise.
DEFAULT_DISTANCE_THRESHOLD = 0.52

def get_retrieval_collection():
    if not os.path.exists(CHROMA_DB_DIR):
        raise FileNotFoundError(f"ChromaDB directory not found at {CHROMA_DB_DIR}. Run build_index.py first.")
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    return client.get_collection(name=COLLECTION_NAME)

def search_provisions(
    query_text: str,
    top_k: int = 5,
    distance_threshold: float = DEFAULT_DISTANCE_THRESHOLD,
    raw_user_input: str = None
) -> list:
    """
    Searches ChromaDB for statutory provisions relevant to query_text.
    Returns list of dicts containing provision text and official metadata.
    Enforces distance threshold and explicit section number validation.
    """
    if not query_text or not query_text.strip():
        return []

    collection = get_retrieval_collection()
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )

    if not results or not results.get("ids") or not results["ids"][0]:
        return []

    ids = results["ids"][0]
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0] if "distances" in results else [0.0] * len(ids)

    # Check if user explicitly demanded a specific section number in query_text or raw_user_input
    combined_query_str = f"{query_text} {raw_user_input or ''}"
    explicit_sec_match = re.search(r"\bsection\s+(\d+[a-z]*)\b", combined_query_str, flags=re.IGNORECASE)
    requested_sec_num = explicit_sec_match.group(1).lower() if explicit_sec_match else None

    retrieved_items = []
    for doc_id, doc_text, meta, dist in zip(ids, documents, metadatas, distances):
        # 1. Distance Threshold Filter
        if distance_threshold is not None and dist > distance_threshold:
            continue

        sec_num = str(meta.get("section_number", "")).lower()

        # 2. Explicit Section Number Validation
        # If user explicitly asked for "Section 999", reject provisions that are not Section 999.
        if requested_sec_num and sec_num != requested_sec_num:
            continue

        item = {
            "document_id": doc_id,
            "distance": round(dist, 4),
            "text": doc_text,
            "law_name": meta.get("law_name"),
            "law_slug": meta.get("law_slug"),
            "section_number": meta.get("section_number"),
            "section_title": meta.get("section_title"),
            "jurisdiction": meta.get("jurisdiction", "India"),
            "source_url": meta.get("source_url"),
            "source_document": meta.get("source_document"),
            "retrieved_date": meta.get("retrieved_date")
        }
        retrieved_items.append(item)

    return retrieved_items

if __name__ == "__main__":
    test_query = "breach of contract and compensation for loss"
    print(f"Testing retrieval for query: '{test_query}'\n")
    matches = search_provisions(test_query, top_k=3)
    for m in matches:
        print(f"[{m['law_name']}] Section {m['section_number']}: {m['section_title']} (Distance: {m['distance']})")
