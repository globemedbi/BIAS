# Chatbot API Contract

**Port:** 8006
**Base URL:** `http://chatbot:8006`

## Endpoints

### POST /api/v1/format
Formats a technical audit result for the specified user_type.

**Request Body:**
```json
{
  "flight_plan": { ... },
  "audit_result": { ... },
  "user_type": "ADJUSTER | MEMBER | ADMIN"
}
```

---

### POST /api/v1/chat
Handles a real-time chat message from a user.

**Request Body:**
```json
{
  "session_id": "uuid",
  "message": "string",
  "user_id": "string",
  "user_type": "ADJUSTER | MEMBER | ADMIN"
}
```

---

### GET /api/v1/chat/history/{session_id}
Returns conversation history for a session.

---

### POST /api/v1/chat/session
Creates a new conversation session.

---

### GET /health
Standard health check.
