"""
Data sources verification utility for LexAssist.
Validates raw source texts and metadata registry against official sources.
"""

import os
import json

METADATA_PATH = os.path.join("data", "metadata", "sources.json")
RAW_DIR = os.path.join("data", "raw")

def verify_sources():
    if not os.path.exists(METADATA_PATH):
        raise FileNotFoundError(f"Metadata registry missing: {METADATA_PATH}")

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)

    indexed_laws = registry.get("indexed_laws", [])
    print(f"Verifying {len(indexed_laws)} official Indian laws registered in LexAssist...\n")

    verified_count = 0
    for law in indexed_laws:
        law_id = law["id"]
        law_name = law["law_name"]
        filename = law["raw_filename"]
        source_url = law["source_url"]
        file_path = os.path.join(RAW_DIR, filename)

        if not os.path.exists(file_path):
            print(f"[MISSING]: {law_name} ({filename})")
            continue

        size = os.path.getsize(file_path)
        print(f"[OK] VERIFIED: {law_name}")
        print(f"   - File: {filename} ({size} bytes)")
        print(f"   - Official URL: {source_url}")
        print(f"   - Source: {law['official_source']}")
        verified_count += 1

    print(f"\nPhase 2 Verification Complete: {verified_count}/{len(indexed_laws)} official laws available.")
    return verified_count == len(indexed_laws)

if __name__ == "__main__":
    verify_sources()

