# LexAssist — System Architecture

## Overview
LexAssist is a local-first, Retrieval-Augmented Generation (RAG) assistant specifically designed to help legal professionals and students locate applicable statutory provisions from indexed official Indian statutes.

## Data Flow Diagram

```text
+-----------------------------------------------------------+
|                        USER (Browser)                     |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                   STREAMLIT INTERFACE                     |
|                 (app.py - Port 8501)                      |
+-----------------------------------------------------------+
                             |
         +-------------------+-------------------+
         | (Text Query)                          | (PDF / Image)
         v                                       v
+------------------------+             +--------------------+
|  Query Preprocessing   |             |  OCR / Extraction  |
+------------------------+             +--------------------+
         |                                       |
         +-------------------+-------------------+
                             v
+-----------------------------------------------------------+
|             ISSUE IDENTIFICATION (Gemini 2.5/Flash)       |
|    - Summarizes facts                                     |
|    - Extracts distinct legal issues                       |
|    - Generates semantic search queries                    |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                  VECTOR RETRIEVAL (ChromaDB)              |
|    - Embeds query                                         |
|    - Queries local collection 'lexassist_provisions'      |
|    - Applies relevance distance threshold                 |
|    - Retrieves top matching sections + official metadata  |
+-----------------------------------------------------------+
                             |
             [Are relevant provisions found?]
                    /                 \
                 [YES]               [NO]
                  /                     \
                 v                       v
+----------------------------------+  +---------------------+
|    CONSTRAINED RAG SYNTHESIS     |  | "No sufficiently    |
| - LLM constrained ONLY to context|  | relevant provision  |
| - Strictly cites exact sections  |  | was found in the    |
| - Prohibits inventing numbers    |  | indexed corpus."    |
+----------------------------------+  +---------------------+
                 \                       /
                  v                     v
+-----------------------------------------------------------+
|                   FINAL STRUCTURED OUTPUT                 |
| 1. Case Summary                                           |
| 2. Legal Issues Identified                                |
| 3. Relevant Legal Provisions (Law, Sec, Text, Official URL)|
| 4. Why Relevant (Grounded reasoning only)                 |
| 5. Important Limitations & Corpus Boundaries              |
| 6. Mandatory Verification Disclaimer                      |
+-----------------------------------------------------------+
```

## Ingestion Pipeline Architecture

```text
[Official India Code PDF]
          |
          v
  extract_text.py (pypdf text extraction + noise removal)
          |
          v
  chunk_laws.py (Regex-based section detector: Sec 1, Sec 2...)
          |
          v
  Structured Chunk JSON + Metadata (Law Name, Sec #, Title, URL)
          |
          v
  build_index.py (Generate deterministic IDs + ChromaDB storage)
          |
          v
  chroma_db/ (Local on-disk vector database)
```

## Component Responsibilities

1. **`ingestion/`**: Loads official statute PDFs, extracts raw text, segments sections cleanly, attaches metadata, and builds local ChromaDB vector collections.
2. **`retrieval/`**: Implements vector search with distance thresholding and metadata formatting.
3. **`analysis/`**: Contains business logic for extracting facts and identifying legal questions.
4. **`llm/`**: Houses the Google Gemini API client configured with strict zero-hallucination system instructions.
5. **`utils/`**: Helper utilities for clean logging, input validation, and markdown generation.
6. **`app.py`**: Streamlit presentation layer connecting inputs directly to the RAG pipeline.
