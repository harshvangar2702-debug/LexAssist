# LexAssist — Architectural Decisions Log

## Decision 1: ChromaDB for Vector Storage
- **Date**: 2026-10-06
- **Decision**: Use ChromaDB running locally (`chroma_db/`).
- **Alternatives Considered**: FAISS, Qdrant Cloud, Pinecone, SQLite with sqlite-vss.
- **Why We Chose This**: ChromaDB is native Python, requires no external server or Docker, persists directly to disk in a local folder, and provides straightforward metadata filtering. Perfect for a university presentation.
- **Consequences**: Local storage is limited to available RAM/disk; ideal for initial MVP corpus.

## Decision 2: Streamlit for User Interface
- **Date**: 2026-10-06
- **Decision**: Build the UI using Streamlit in `app.py`.
- **Alternatives Considered**: React/Next.js frontend with FastAPI backend, Gradio, Flask + HTML templates.
- **Why We Chose This**: A single Python file (`app.py`) can handle state, file uploads, layout, and rendering without requiring Node.js, npm, or complex API wiring. A student with minimal coding experience can understand, run, and modify it immediately.
- **Consequences**: Synchronous execution model; UI re-runs on state interaction, easily managed with Streamlit session state.

## Decision 3: Google Gemini API via official `google-genai` SDK
- **Date**: 2026-10-06
- **Decision**: Use the official `google-genai` Python library.
- **Alternatives Considered**: OpenAI API, Anthropic Claude API, local Ollama LLMs.
- **Why We Chose This**: Superior multimodal support (reading uploaded case PDFs and photos of documents directly), strong reasoning capabilities, fast response times, and generous free tier for academic evaluation.
- **Consequences**: Requires an internet connection and a valid `GEMINI_API_KEY` stored in `.env`.

## Decision 4: Semantic Legal Provision-Level Chunking
- **Date**: 2026-10-06
- **Decision**: Split statutory texts by Section/Article boundaries rather than fixed token/character windows (e.g. 500 characters).
- **Alternatives Considered**: Recursive character text splitting, fixed token chunking with overlap.
- **Why We Chose This**: In legal analysis, a legal provision (e.g., Section 73 of the Indian Contract Act) is a discrete semantic unit. Arbitrary character cuts bisect provisions, separate illustrations from rules, and destroy legal context.
- **Consequences**: Chunks have variable length, but maintain 100% legal integrity and clean citation traceability.

## Decision 5: Official India Code Government Sources Only
- **Date**: 2026-10-06
- **Decision**: Restrict source corpus strictly to official legislative PDFs from `indiacode.nic.in`.
- **Alternatives Considered**: Unverified legal blogs, student revision websites, Wikipedia, generic web scraping.
- **Why We Chose This**: Legal safety demands official authenticity. Secondary blogs may contain commentary, errors, or outdated amendments.
- **Consequences**: Text extraction from government scanned/typeset PDFs requires clean preprocessing, which we handle in Phase 3.

## Decision 6: Environment Isolation with Python 3.11
- **Date**: 2026-10-06
- **Decision**: Use `py -3.11 -m venv .venv` instead of the system default Python 3.14.
- **Alternatives Considered**: System Python 3.14.
- **Why We Chose This**: ChromaDB and many scientific wheels (`onnxruntime`, `pydantic-core`) lack prebuilt binary wheels for Python 3.14 on Windows, leading to compilation errors. Python 3.11 is fully mature and universally supported.
- **Consequences**: Virtual environment must be activated explicitly with Python 3.11 binaries.
