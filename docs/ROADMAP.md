# LexAssist — Master 12-Phase Roadmap

This roadmap tracks the development of LexAssist through small, thoroughly tested, explainable phases.

---

### [x] Phase 1 — Project Setup & Environment Verification
- [x] Create project structure and subdirectories.
- [x] Setup `.gitignore`, `.env.example`, `requirements.txt`.
- [x] Author comprehensive persistent documentation suite in `docs/`.
- [ ] Initialize Python 3.11 virtual environment (`.venv`).
- [ ] Install pinned dependencies and run baseline smoke test.
- [ ] Implement baseline Streamlit interface (`app.py`).
- [ ] Verify local launch on `http://localhost:8501`.

---

### [ ] Phase 2 — Legal Data Collection
- [ ] Select 3 official Indian statutes from India Code (`indiacode.nic.in`):
  1. Indian Contract Act, 1872
  2. Information Technology Act, 2000
  3. Consumer Protection Act, 2019
- [ ] Download official PDFs into `data/raw/`.
- [ ] Record provenance, date, and URLs in `data/metadata/sources.json` and `docs/DATA_SOURCES.md`.
- [ ] Test access and file integrity.

---

### [ ] Phase 3 — Text Extraction Pipeline
- [ ] Build `ingestion/extract_text.py` using `pypdf`.
- [ ] Strip scanning noise, repeated running headers/footers, and page numbers.
- [ ] Save clean text in `data/processed/`.
- [ ] Test extraction with automated verification script.

---

### [ ] Phase 4 — Legal Provision Chunking
- [ ] Build `ingestion/chunk_laws.py`.
- [ ] Implement robust section-boundary regex parsing (`Section \d+`, marginal notes).
- [ ] Retain provisions, explanations, and illustrations in one coherent chunk.
- [ ] Generate metadata payload for each provision.
- [ ] Test that chunking preserves section numbering correctly.

---

### [ ] Phase 5 — ChromaDB Vector Store
- [ ] Build `ingestion/build_index.py`.
- [ ] Generate deterministic IDs: `{law_slug}_sec_{number}`.
- [ ] Store chunks and metadata in local `chroma_db/`.
- [ ] Test count of indexed provisions against expected count.

---

### [ ] Phase 6 — Semantic Retrieval Engine
- [ ] Build `retrieval/search.py`.
- [ ] Implement similarity search with distance thresholding.
- [ ] Filter out provisions failing minimum relevance threshold.
- [ ] Author `tests/test_retrieval.py` and run benchmark queries.

---

### [ ] Phase 7 — Gemini Client Integration
- [ ] Build `llm/gemini_client.py` using `google-genai` SDK.
- [ ] Configure environment variable loading with `python-dotenv`.
- [ ] Set up system instructions emphasizing zero hallucination.
- [ ] Test connectivity and error handling.

---

### [ ] Phase 8 — Grounded RAG Synthesis & Guardrails
- [ ] Build `analysis/case_analysis.py`.
- [ ] Connect Question -> Retrieval -> Constrained Gemini prompt -> Structured Answer.
- [ ] Implement Negative Tests (Test A, B, C, D) to prove the model never hallucinates.

---

### [ ] Phase 9 — Multimodal File & Image Input
- [ ] Add PDF and scanned image upload processing in Streamlit.
- [ ] Extract facts and trigger RAG pipeline from uploaded case briefs.
- [ ] Test with sample case PDF and document photo.

---

### [ ] Phase 10 — Streamlit UI Finalization
- [ ] Polish UI with professional legal styling.
- [ ] Display sidebar with corpus statistics and official sources.
- [ ] Implement expandable cards for retrieved provisions and official India Code links.
- [ ] Add prominent disclaimer banner.

---

### [ ] Phase 11 — Security, Logging & Hardening
- [ ] Sanitize logging to ensure zero API key leakage.
- [ ] Add robust user-friendly error banners.
- [ ] Validate `.env` and `.gitignore` defenses.

---

### [ ] Phase 12 — University Presentation Preparation
- [ ] Create `docs/PRESENTATION.md` with demo slides outline.
- [ ] Write step-by-step presentation script with test scenarios.
- [ ] Prepare anticipated Q&A defense for academic evaluators.
