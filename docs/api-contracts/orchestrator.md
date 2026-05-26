# Orchestrator API Contract

**Port:** 8001
**Base URL:** `http://orchestrator:8001`

## Endpoints

### POST /plan/create
Creates a new Flight Plan for a claim request.

**Request Body:**
```json
{
  "claim_id": "string",
  "member_id": "string",
  "request_type": "CLAIM_AUDIT | DOC_ANONYMIZATION | CLAIM_STATUS",
  "file_uris": ["string"],
  "priority": "NORMAL | HIGH | URGENT"
}
```

**Response:** `202 Accepted`
```json
{
  "status": "ACCEPTED",
  "service": "ORCHESTRATOR",
  "job_id": "uuid",
  "poll_url": "/plan/{plan_id}/status"
}
```

---

### POST /plan/{plan_id}/stage/update
Updates a stage within an existing Flight Plan.

**Request Body:**
```json
{
  "stage": 1,
  "status": "COMPLETED | FAILED",
  "output_uri": "string (optional)"
}
```

---

### GET /plan/{plan_id}/status
Returns current execution state of a Flight Plan.

---

### POST /plan/{plan_id}/recover
Triggers Stage 99 recovery for a failed plan.

---

### POST /registry/register
Registers a service with its URL and health status.

---

### GET /registry
Returns all registered services and their health status.

---

### GET /metrics
Returns system-level metrics for the BI dashboard.

---

### GET /health
Standard health check.
