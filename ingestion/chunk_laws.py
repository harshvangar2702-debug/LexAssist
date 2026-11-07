"""
Legal Provision Chunking Module for LexAssist.
Parses statutory text into section-level chunks with complete official metadata.
"""

import os
import re
import json
from datetime import datetime
from ingestion.extract_text import extract_raw_text

METADATA_PATH = os.path.join("data", "metadata", "sources.json")
RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")

def load_sources_registry():
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def chunk_statute(law_info: dict) -> list:
    """
    Parses statutory text into section chunks.
    Splits by Section headings (e.g. 'Section 1.', 'Section 73.').
    """
    raw_filename = law_info["raw_filename"]
    raw_file_path = os.path.join(RAW_DIR, raw_filename)

    full_text = extract_raw_text(raw_file_path)

    # Regex matching "Section <number>[letter]. <Title>"
    # Matches patterns like:
    # "Section 73. Compensation for loss..." or "Section 66C. Punishment for..."
    section_pattern = r"(?:^|\n)(Section\s+(\d+[A-Z]*)\.\s*([^\n]+))"

    matches = list(re.finditer(section_pattern, full_text, flags=re.MULTILINE))

    chunks = []
    if not matches:
        print(f"Warning: No explicit Section headings detected in {raw_filename}")
        return chunks

    for i in range(len(matches)):
        start_idx = matches[i].start(1)
        end_idx = matches[i+1].start(1) if (i + 1 < len(matches)) else len(full_text)

        sec_header_full = matches[i].group(1).strip()
        sec_num = matches[i].group(2).strip()
        sec_title = matches[i].group(3).strip()

        chunk_text = full_text[start_idx:end_idx].strip()

        # Deterministic document ID
        law_slug = law_info["id"]
        doc_id = f"{law_slug}_sec_{sec_num.lower()}"

        chunk = {
            "document_id": doc_id,
            "text": chunk_text,
            "law_name": law_info["law_name"],
            "law_slug": law_slug,
            "section_number": sec_num,
            "section_title": sec_title,
            "article_number": None,
            "article_title": None,
            "jurisdiction": law_info.get("jurisdiction", "India"),
            "source_url": law_info["source_url"],
            "source_document": raw_filename,
            "retrieved_date": datetime.now().strftime("%Y-%m-%d"),
        }
        chunks.append(chunk)

    return chunks

def process_all_laws():
    """Processes all registered laws in sources.json into processed JSON chunks."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    registry = load_sources_registry()

    all_chunks = []
    for law in registry.get("indexed_laws", []):
        chunks = chunk_statute(law)
        output_file = os.path.join(PROCESSED_DIR, f"{law['id']}_chunks.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        print(f"Parsed {len(chunks)} sections for '{law['law_name']}' -> saved to {output_file}")
        all_chunks.extend(chunks)

    # Master index file
    master_file = os.path.join(PROCESSED_DIR, "all_provisions_chunks.json")
    with open(master_file, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\nPhase 4 Chunking Complete: {len(all_chunks)} total provisions chunked into {master_file}")
    return all_chunks

if __name__ == "__main__":
    process_all_laws()

