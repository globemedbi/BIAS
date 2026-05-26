# DB Agent API Contract

**Port:** 8003
**Base URL:** `http://db-agent:8003`

All endpoints require: `X-Service-Token` and `X-Service-Name` headers.

## Endpoints

### POST /claims/store
Stores OCR extraction results.

### POST /authorization/fetch
Fetches authorization and coverage records for a claim.

### POST /claims/history
Returns member claim history.

### POST /query/nl
Translates natural language query to SQL and executes it.

**Safety:** SELECT only. Whitelisted tables. All input sanitized.

### POST /logs/audit
Writes an audit log entry. Called by all services.

### POST /registry/save
Persists the Orchestrator service registry.

### GET /registry/load
Loads the persisted service registry.

### GET /health
Standard health check.
