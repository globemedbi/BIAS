# BIAS Flow Diagrams

## Claim Audit Flow

```
[External Caller]
      │
      │ POST /api/v1/claims/submit (JWT + files)
      ▼
[Communicator :8000]
      │ Upload files to object storage
      │ POST /plan/create
      ▼
[Orchestrator :8001]
      │ Build Flight Plan from template
      │ Inject service registry URLs
      │ Persist plan via DB Agent
      │ Return plan_id
      ▼
[Communicator :8000]
      │ Return 202 Accepted + poll_url to caller
      │
      │ (async — Flight Plan takes over)
      ▼
[File Management :8002]
      │ Download files from object storage
      │ OCR → Anonymize → Translate
      │ Store artifacts
      ▼
[Claims Expert :8004]
      │ Fetch OCR text from File Management
      │ Fetch auth records from DB Agent
      │ Call LLM Agent for summarization
      │ Call LLM Agent for reconciliation
      │ Generate Master Summary
      ▼
[Chatbot :8006]
      │ Format result per user_type
      │ Call LLM Agent for tone adaptation
      │ POST /internal/v1/callback to Communicator
      ▼
[Communicator :8000]
      │ Store result for polling
      ▼
[External Caller]
      GET /api/v1/claims/{request_id}/status → COMPLETED
      GET /api/v1/claims/{request_id}/report → Master Summary
```

## Stage 99 Error Recovery Flow

```
[Any Service]
      │ Unrecoverable error
      ▼
[Orchestrator :8001]
      POST /plan/{id}/recover
      │ Update Flight Plan overall_status = FAILED_RETRYING
      │ Notify DB Agent to log error
      │ Attempt recovery from last successful stage
```
