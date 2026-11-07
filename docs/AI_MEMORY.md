# LexAssist AI Memory

## Project Purpose
LexAssist is an AI-powered Legal Research Assistant designed to assist lawyers, law students, and legal researchers in discovering potentially relevant legal provisions from an indexed collection of official statutory documents.
It is built as an explainable, local-first research aid for a university presentation.
It is NOT a replacement for a lawyer, not a source of legal advice, and strictly adheres to a **Zero-Hallucination Legal Safety Rule**.

## Current Architecture
Local-first Retrieval-Augmented Generation (RAG) with Persistent Session Management:
1. User provides legal query or uploads case file (PDF/Image) via Streamlit UI.
2. Fact and legal issue extraction identifies key issues.
3. Query generation searches ChromaDB for matching statutory provisions.
4. Top official provisions are retrieved along with provenance metadata.
5. Google Gemini API synthesizes a structured analysis strictly grounded in the retrieved legal provisions.
6. The user receives a structured breakdown: Case Summary, Legal Issues, Exact Provisions with Official Citations, Why Relevant, Limitations, and Disclaimer.
7. Interactive multi-turn chat allows the user to converse on the analyzed case with auto-scroll and professional legal avatars (`🧑‍💼`, `⚖️`).
8. All conversations and case analyses are persistently saved to local disk (`data/chats/`) with thread branching and sidebar history navigation.

## Technology Stack
- **Language**: Python 3.11.9 (via `py -3.11`)
- **Frontend / UI**: Streamlit 1.65.0
- **Vector Database**: ChromaDB 1.5.9 (local persistence in `chroma_db/`)
- **Chat Persistence**: JSON-based file storage in `data/chats/` with atomic write semantics (`os.replace`)
- **LLM / Generation**: Google Gemini API via official SDK (`google-genai` 2.28.0)
- **PDF Extraction**: `pypdf` 6.19.0
- **Image Processing**: `pillow` 12.3.0
- **Environment Management**: `python-dotenv` 1.2.4

## Completed Features
- Modular project structure (`ingestion/`, `retrieval/`, `analysis/`, `llm/`, `utils/`, `tests/`, `data/`, `docs/`).
- Persistent chat session storage (`utils/chat_storage.py`) in `data/chats/`.
- Sidebar chat history with timestamps, message counts, and case snippets.
- Two distinct New Chat actions:
  - `➕ New Chat on Same Case` (creates a clean thread for the current case).
  - `🔄 New Chat on Different Case` (clears everything for a new dispute).
- Professional legal role avatars (`🧑‍💼` for Legal Counsel / User, `⚖️` for Official Scales of Justice / Assistant).
- Smooth automatic scrolling to the chat section upon submitting messages.
- Full test suite:
  - `tests/test_chat_storage.py` (9/9 passed)
  - `tests/test_retrieval.py` (3/3 passed)
  - `tests/test_analysis.py` (4/4 passed)

## Database Structure
ChromaDB Collection: `lexassist_provisions` (34 indexed sections)
Chat Storage: `data/chats/{session_id}.json`

## Indexed Laws
1. **The Indian Contract Act, 1872** (17 sections)
2. **The Information Technology Act, 2000** (10 sections)
3. **The Consumer Protection Act, 2019** (7 sections)

## Official Data Sources
- **Primary Portal**: India Code Digital Repository (`https://www.indiacode.nic.in`)

## Environment Variables
- `GEMINI_API_KEY`: API key for Google Gemini model calls (stored in `.env`, never committed).

## Current Tests
- `tests/test_chat_storage.py`: 9/9 tests PASSED.
- `tests/test_retrieval.py`: 3/3 scenarios PASSED.
- `tests/test_analysis.py`: 4/4 anti-hallucination scenarios PASSED.

## UI & Presentation Design System
- Modern Legal Typography: Google Web Fonts (`Cinzel` display face, `Plus Jakarta Sans` body, `JetBrains Mono` statutory quotes).
- Authoritative Color Palette: Oxford Deep Navy (`#0B192C`), Slate Blue (`#1E3E62`), Antique Gold (`#C5A059`), Emerald Verification (`#0F766E`), Warm Amber Caveat (`#B45309`).
- Hero Header Banner: Embedded insignia seal, central Central Acts badges, and zero-hallucination indicators.
- Instant Demo Presets: 3 one-click case buttons for instant live testing (Contract Breach, Defective Product Injury, Unauthorized Cyber Data Theft).
- Tabbed Analysis View: Tabs for Executive Summary, Retrieved Provisions, Relevance Rationale, and Statutory Disclaimer.
- Interactive Grounded Chat: Lawyer (`🧑‍💼`) and Judicial Scales (`⚖️`) avatars, persistent thread context pills, and auto-scroll.

## Legal Safety Rules
- NEVER invent an article, section, law, or citation.
- Always include the mandatory legal verification disclaimer.

