# File Management API Contract

**Port:** 8002
**Base URL:** `http://file-management:8002`

## Endpoints

### POST /api/v1/process
Submits files for OCR → Anonymize → Translate pipeline. Returns 202 immediately.

**Request Body:**
```json
{
  "flight_plan": { ... },
  "file_uris": ["string"],
  "translate": false,
  "target_language": "en"
}
```

**Response:** `202 Accepted`
```json
{
  "status": "ACCEPTED",
  "service": "FILE_MANAGEMENT",
  "job_id": "uuid",
  "poll_url": "/api/v1/process/status/{job_id}"
}
```

---

### GET /api/v1/process/status/{job_id}
Returns the processing status and output URIs when complete.

---

### GET /api/v1/extract/{claim_id}
Returns the extracted text artifacts for a claim.

---

### GET /health
Standard health check.
