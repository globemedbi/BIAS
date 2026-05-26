# File Management Service

**Port:** 8002 | **Owner:** Backend Dev | **Category:** Document Pipeline

## Responsibility
Transforms raw documents into structured, anonymized, translated text artifacts.
Pipeline order: OCR → Anonymize → Translate (STRICT — never change).

## Key Files
- `ocr/ocr_engine.py` — External OCR client
- `anonymizer/anonymizer.py` — PII removal (MUST run before translation)
- `translator/translator.py` — Optional translation
- `agent/file_agent.py` — Pipeline orchestrator

## Running Locally
```bash
cd file-management
pip install -r requirements.txt
uvicorn api.main:app --port 8002 --reload
```

## API
See `docs/api-contracts/file-management.md`
