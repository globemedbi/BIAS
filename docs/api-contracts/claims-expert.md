# Claims Expert API Contract

**Port:** 8004
**Base URL:** `http://claims-expert:8004`

## Endpoints

### POST /api/v1/audit
Triggers a full claim audit. Returns 202 immediately.

**Request Body:**
```json
{
  "flight_plan": { ... }
}
```

**Response:** `202 Accepted`
```json
{
  "status": "ACCEPTED",
  "service": "CLAIMS_EXPERT",
  "job_id": "uuid",
  "poll_url": "/api/v1/audit/status/{audit_id}"
}
```

---

### GET /api/v1/audit/status/{audit_id}
Returns the audit processing status.

---

### GET /api/v1/summary/{claim_id}
Returns the Master Summary for a completed claim audit.

**Decision values:**
- `APPROVED`: within_policy=true, discrepancies=none or LOW
- `PENDING_REVIEW`: within_policy=true, discrepancies=MEDIUM
- `REJECTED`: within_policy=false OR discrepancies=HIGH

---

### POST /api/v1/validate/policy
Validates a claim against policy rules.

---

### GET /health
Standard health check.
