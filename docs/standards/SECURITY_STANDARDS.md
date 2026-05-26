# BIAS Security Standards

## Credential Management
- All secrets via environment variables only
- `.env` never committed to git
- `.env.example` is the only committed env template
- No partial key logging (not even first/last characters)

## Authentication
- External: JWT, validated on every request, never cached
- Internal: `X-Service-Token` shared secret, validated on every request

## Input Validation
- All external inputs validated via Pydantic models
- DB Agent: NL2SQL input sanitized, SELECT only, table whitelist
- LLM Agent: prompts sanitized for injection before sending to provider

## PII Handling
- Anonymizer runs before any external service (translation, LLM)
- No PII in any log output — mask or omit
- No PII in API response bodies unless explicitly authorized

## Dependency Scanning
- `bandit` runs on every PR (medium+ severity)
- TruffleHog scans every PR for secrets

## Network
- Only Communicator (:8000) exposed externally
- All inter-service traffic on `bias-network` bridge
- Rate limiting enforced at Communicator boundary

## Incident Response
- All audit events written to Logging DB via DB Agent
- Log format is structured JSON for SIEM compatibility
- Every unhandled exception logged with `request_id` for tracing
