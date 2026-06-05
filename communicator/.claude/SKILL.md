# Communicator Service — Claude Code Skill File

## Identity
- Name: COMMUNICATOR
- Port: 8000
- Owner: Backend Dev
- Category: External Gateway

## Exact Responsibility
The Communicator is the ONLY service exposed to the outside world.
It validates, packages, and routes. Nothing more.

## What This Service Does
1. Exposes external FastAPI endpoints to .NET applications
2. Validates JWT on every inbound external request
3. Enforces rate limiting per client
4. Uploads files to object storage immediately on receipt
5. Calls Orchestrator to create a Flight Plan
6. Tracks claim progress via session store
7. Returns 202 Accepted immediately to caller
8. Receives callback from Chatbot when processing completes
9. Makes result available for polling

## What This Service Must NEVER Do
- Contain any business logic
- Inspect or process claim content
- Make routing decisions (Orchestrator does this)
- Call DB Agent, LLM Agent, File Management, Claims Expert, or Chatbot directly
- Store files on local disk (always object storage)
- Hardcode any service URL

## API Endpoints to Implement
External:
- POST /api/v1/claims/submit
- GET  /api/v1/claims/{request_id}/status
- GET  /api/v1/claims/history
- GET  /api/v1/claims/{request_id}/report
- GET  /api/v1/health

Internal:
- POST /internal/v1/callback
- GET  /internal/v1/health

## JWT Validation Rules
- Validate on every external endpoint
- Use JWT_SECRET_KEY from environment
- Return 401 with standard ErrorResponse if invalid
- Never log token values

## Rate Limiting Rules
- Per X-Client-ID header
- Default: 100 requests per minute
- Return 429 with retry_after_s field if exceeded

## Session Tracking
- In-memory dict for Phase 1
- Key: request_id, Value: {plan_id, claim_id, status, result}
- TTL: 24 hours
- Never persist session data to disk

## Error Handling
- 503 if Orchestrator unreachable (circuit break immediately)
- 400 for validation failures (return field-level errors)
- All errors use ErrorResponse from shared.models.response

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use Claim model from shared.models.claim
- Use BaseResponse, ErrorResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
