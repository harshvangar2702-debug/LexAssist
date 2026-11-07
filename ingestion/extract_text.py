"""
Text Extraction Module for LexAssist.
Handles extracting clean text from raw files (.pdf or .txt) and removing extraction noise.
"""

import os
import re
from pypdf import PdfReader

def extract_raw_text(file_path: str) -> str:
    """Extract raw text from PDF or TXT file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Source file not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            extracted_pages.append(text)
        raw_text = "\n".join(extracted_pages)
    else:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

    return clean_text_noise(raw_text)

def clean_text_noise(text: str) -> str:
    """Remove common header/footer noise, page numbers, and excess whitespace."""
    # Normalize carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove running header/footer patterns like "Page 1 of 45" or "[SEC. 1]"
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", "", text, flags=re.IGNORECASE)

    # Normalize multiple newlines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()

if __name__ == "__main__":
    test_path = os.path.join("data", "raw", "indian_contract_act_1872.txt")
    if os.path.exists(test_path):
        cleaned = extract_raw_text(test_path)
        print(f"Extracted clean text ({len(cleaned)} chars) from {test_path}")

