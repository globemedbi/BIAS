# BIAS Security Architecture

## Authentication & Authorization

### External (Communicator boundary)
- JWT validation on every external endpoint
- Token signed with `JWT_SECRET_KEY` from environment
- Algorithm: HS256 (configurable via `JWT_ALGORITHM`)
- Expiry: 60 minutes default (configurable via `JWT_EXPIRY_MINUTES`)

### Internal (service-to-service)
- `X-Service-Token` header on every internal call
- Shared secret from `INTERNAL_SERVICE_TOKEN` environment variable
- `X-Service-Name` header identifies caller for audit logging

## Data Protection

### PII Handling
- Anonymizer runs BEFORE any external translation engine
- No PII is logged anywhere in any service
- DB Agent does not return raw PII to unauthorized callers
- Chatbot enforces member-level data isolation

### Credentials
- No credentials in code — environment variables only
- No credentials in logs — masked or omitted
- `.env` excluded from git via `.gitignore`
- LLM API keys isolated to LLM Agent only
- Database credentials isolated to DB Agent only

## Network Security

### Service Isolation
- All services on `bias-network` Docker bridge network
- Only Communicator (:8000) exposed externally
- All other services communicate internally only

### Rate Limiting
- Communicator enforces per-client rate limiting
- Default: 100 requests/minute per `X-Client-ID`
- Returns 429 with `retry_after_s` on breach

## Scanning & Monitoring

- `bandit` static analysis in CI/CD pipeline
- TruffleHog secret scanning on every PR
- Structured JSON logging for SIEM integration
- Audit log written to Logging DB for every operation
