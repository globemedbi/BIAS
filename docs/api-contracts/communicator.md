# Communicator API Contract

**Port:** 8000
**Base URL:** `http://communicator:8000`

## External Endpoints (JWT required)

### POST /api/v1/claims/submit
Submits a new claim for processing. Returns 202 immediately.

**Headers:** `Authorization: Bearer <jwt>`

**Request:** `multipart/form-data`
- `claim_id`: string
- `member_id`: string
- `claim_type`: MEDICAL | DENTAL | VISION | PHARMACY
- `files[]`: file attachments

**Response:** `202 Accepted`
```json
{
  "status": "ACCEPTED",
  "service": "COMMUNICATOR",
  "job_id": "uuid",
  "poll_url": "/api/v1/claims/{request_id}/status"
}
```

---

### GET /api/v1/claims/{request_id}/status
Polls the status of a submitted claim.

---

### GET /api/v1/claims/history
Returns claim history for the authenticated user.

---

### GET /api/v1/claims/{request_id}/report
Returns the final Master Summary report.

---

### GET /api/v1/health
External health check.

---

## Internal Endpoints

### POST /internal/v1/callback
Receives final result from Chatbot.

**Headers:** `X-Service-Token: <token>`, `X-Service-Name: CHATBOT`

---

### GET /internal/v1/health
Internal health check.
