# LexAssist — Database Schema Specification

## Vector Database: ChromaDB

- **Storage Location**: Local directory `./chroma_db/`
- **Default Collection Name**: `lexassist_provisions`
- **Embedding Model**: Default sentence embeddings or Gemini embeddings (`text-embedding-004`).

## Record Schema

Each record stored in the `lexassist_provisions` ChromaDB collection corresponds to exactly one statutory provision (Section or Article).

| Field | Type | Description | Example |
|---|---|---|---|
| `id` | String | Deterministic unique identifier: `{law_slug}_sec_{number}` | `contract_act_1872_sec_73` |
| `document` | String | The complete statutory text of the section including explanations and illustrations. | "When a contract has been broken, the party who suffers by such breach is entitled to receive..." |
| `metadata.law_name` | String | Full formal name of the enactment | "The Indian Contract Act, 1872" |
| `metadata.law_slug` | String | Slugified short name for grouping | "contract_act_1872" |
| `metadata.section_number`| String | Section or Article identifier | "73" |
| `metadata.section_title` | String | Marginal note or title of the section | "Compensation for loss or damage caused by breach of contract" |
| `metadata.jurisdiction`  | String | Legal jurisdiction | "India" |
| `metadata.source_url`    | String | Official India Code repository link | "https://www.indiacode.nic.in/handle/123456789/2187" |
| `metadata.source_document` | String | Source document file name | "indian_contract_act_1872.pdf" |
| `metadata.retrieved_date`| String | Date document was fetched (ISO 8601) | "2026-10-06" |

## ID Determinism
To prevent duplicate records upon re-ingestion, chunk IDs are generated deterministically using:
```python
clean_law_slug = law_slug.lower().replace(" ", "_")
clean_sec_num = str(section_number).strip().lower().replace(" ", "_")
record_id = f"{clean_law_slug}_sec_{clean_sec_num}"
```
This guarantees idempotent updates: running ingestion multiple times updates existing records in place rather than bloating the database with duplicate embeddings.
