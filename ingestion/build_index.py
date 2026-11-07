"""
ChromaDB Vector Indexing Module for LexAssist.
Reads processed provision chunks and populates the local ChromaDB database.
"""

import os
import json
import chromadb

CHROMA_DB_DIR = os.path.join(".", "chroma_db")
PROCESSED_FILE = os.path.join("data", "processed", "all_provisions_chunks.json")
COLLECTION_NAME = "lexassist_provisions"

def get_chroma_client():
    """Returns persistent local ChromaDB client."""
    os.makedirs(CHROMA_DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=CHROMA_DB_DIR)

def build_vector_index():
    """Loads processed provisions and upserts them into ChromaDB with deterministic IDs."""
    if not os.path.exists(PROCESSED_FILE):
        raise FileNotFoundError(f"Processed chunks file missing: {PROCESSED_FILE}. Run chunk_laws.py first.")

    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        print("No provisions found to index.")
        return 0

    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    ids = []
    documents = []
    metadatas = []

    for item in chunks:
        ids.append(item["document_id"])
        documents.append(item["text"])

        # Sanitize metadata for ChromaDB (no null values allowed in metadata dict)
        meta = {
            "law_name": str(item["law_name"]),
            "law_slug": str(item["law_slug"]),
            "section_number": str(item["section_number"]),
            "section_title": str(item["section_title"]),
            "article_number": str(item["article_number"] or ""),
            "article_title": str(item["article_title"] or ""),
            "jurisdiction": str(item["jurisdiction"]),
            "source_url": str(item["source_url"]),
            "source_document": str(item["source_document"]),
            "retrieved_date": str(item["retrieved_date"]),
        }
        metadatas.append(meta)

    # Upsert into ChromaDB
    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    total = collection.count()
    print(f"Phase 5 Vector Indexing Complete: Successfully indexed {len(ids)} provisions into ChromaDB '{COLLECTION_NAME}' collection.")
    print(f"Total active records in local database: {total}")
    return total

if __name__ == "__main__":
    build_vector_index()

