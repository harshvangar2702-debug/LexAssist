# LexAssist — Privacy and Document Handling Policy

## Purpose
In legal research, case documents, FIRs, contracts, and petitions frequently contain highly confidential personal data, trade secrets, and non-public dispute details. LexAssist is engineered to respect strict privacy principles.

---

## 1. Local-First Processing
- **Vector Storage**: All indexed laws and vector embeddings reside 100% locally on your computer inside the `./chroma_db/` folder.
- **No Cloud Database**: No user queries or legal texts are sent to third-party vector clouds (e.g., Pinecone, AWS).
- **Temporary Document Extraction**: Files uploaded via the Streamlit interface (PDFs, images) are processed in memory and written only to temporary scratch locations if needed for OCR. They are deleted after session completion.

---

## 2. External API Transmission (Gemini API)
- When a user asks a question or submits case facts, the extracted summary and the retrieved legal provisions are transmitted securely over TLS (HTTPS) to the Google Gemini API to formulate the synthesized legal reasoning.
- **Enterprise / Developer Privacy**: Under Google AI Studio paid tiers and standard enterprise terms, submitted prompt content is not used to train base foundation models.
- **Anonymization Recommendation**: Users are strongly advised in the UI disclaimer to redact personally identifiable information (parties' real names, Aadhaar numbers, bank account numbers, physical addresses) before uploading real dispute documents.

---

## 3. Logging Sanitation
- The system logs processing milestones, retrieval metrics, and error codes.
- **Strict Prohibition**: The logging module is programmed never to record:
  - User API keys (`GEMINI_API_KEY`)
  - Full text of private uploaded case petitions
  - Any personally identifying credentials
