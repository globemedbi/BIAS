# File Management Service — Claude Code Skill File

## Identity
- Name: FILE_MANAGEMENT
- Port: 8002
- Owner: Backend Dev
- Category: Document Pipeline

## Exact Responsibility
File Management transforms raw documents into
structured, anonymized, translated text artifacts.
It manages the OCR → Anonymize → Translate pipeline.

## What This Service Does
1. Receives file URIs from object storage
2. Downloads and processes files through OCR engine
3. Passes OCR output through Anonymizer (removes PII)
4. Optionally translates anonymized text
5. Validates output integrity at each stage
6. Stores results in object storage
7. Returns job_id immediately (202 pattern)
8. Exposes status polling endpoint

## What This Service Must NEVER Do
- Store files on local disk permanently
- Pass non-anonymized data to any external translation engine
- Call DB Agent, LLM Agent, Claims Expert, or Chatbot
- Return PII-containing text in API responses
- Skip anonymization even if translation is not needed

## Pipeline Order (STRICT — never change)
1. Download file from object storage
2. Run OCR extraction
3. Run Anonymization (ALWAYS before translation)
4. Run Translation (if requested)
5. Validate output integrity (count pages, check text loss)
6. Upload results to object storage
7. Return output URIs

## Fallback Rules
- If Translator fails: return Anonymized-only result (partial success)
- If Anonymizer fails: STOP — do not proceed to translation
- If OCR fails: STOP — raise to Stage 99

## API Endpoints to Implement
- POST /api/v1/process
- GET  /api/v1/process/status/{job_id}
- GET  /api/v1/extract/{claim_id}
- GET  /health

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, AcceptedResponse from shared.models.response
- Job state stored in memory (dict keyed by job_id) for Phase 1
- All functions must have type hints and docstrings
- Minimum 80% test coverage
