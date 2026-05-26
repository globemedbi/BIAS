# LLM Agent API Contract

**Port:** 8005
**Base URL:** `http://llm-agent:8005`

All endpoints require: `X-Service-Token` and `X-Service-Name` headers.

## Endpoints

### POST /api/v1/complete
Sends a completion request to the configured LLM provider.

**Request Body:**
```json
{
  "task_type": "summarize | audit | reconcile | chat | extract",
  "model_preference": "FAST | BALANCED | POWERFUL",
  "context": "string",
  "input": "string",
  "max_tokens": 1000
}
```

**Response:**
```json
{
  "status": "SUCCESS",
  "service": "LLM_AGENT",
  "data": {
    "content": "string",
    "model_used": "string",
    "tokens_used": 123,
    "cached": false
  }
}
```

---

### POST /api/v1/embed
Generates vector embeddings for the provided text.

---

### GET /api/v1/models
Returns available models and their current status.

---

### GET /api/v1/usage/report
Returns token usage statistics per calling service.

---

### GET /health
Standard health check.
