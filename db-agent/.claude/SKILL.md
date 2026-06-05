# DB Agent Service — Claude Code Skill File

## Identity
- Name: DB_AGENT
- Port: 8003
- Owner: DB Specialist
- Category: Data Domain

## Exact Responsibility
The DB Agent is the ONLY service that touches any database.
All other services request data through this service.
No other service has database credentials.

## What This Service Does
1. Routes data requests to correct database (Legacy, DWH, Vector, Logging)
2. Stores OCR extraction results from File Management
3. Fetches authorization and coverage records for Claims Expert
4. Returns member claim history for Claims Expert and Chatbot
5. Translates natural language queries to SQL for Chatbot
6. Writes all audit log entries for all services
7. Persists and loads the Orchestrator service registry

## What This Service Must NEVER Do
- Expose raw database credentials to any other service
- Accept or execute raw SQL from other services
- Return un-sanitized data that contains PII to unauthorized callers
- Call LLM Agent, File Management, Claims Expert, or Chatbot
- Skip writing to the audit log when requested

## API Endpoints to Implement
- POST /claims/store
- POST /authorization/fetch
- POST /claims/history
- POST /query/nl
- POST /logs/audit
- POST /registry/save
- GET  /registry/load
- GET  /health

## Database Routing Rules
- OCR results → Vector DB + Legacy DB
- Authorization data → Legacy DB
- Claim history → Legacy DB
- NL2SQL queries → Legacy DB or DWH
- Audit logs → Logging DB
- Registry → Logging DB

## NL2SQL Safety Rules
- Whitelist of allowed tables only
- No DELETE, UPDATE, DROP, ALTER allowed
- Sanitize all user input before translation
- Log every NL2SQL query to audit log

## Internal Call Validation
- Validate X-Service-Token header on every request
- Validate X-Service-Name header matches allowed callers
- Return 401 if token invalid

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, ErrorResponse from shared.models.response
- Each database connector in its own module
- All functions must have type hints and docstrings
- Minimum 80% test coverage
