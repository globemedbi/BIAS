# Claims Expert Service — Claude Code Skill File

## Identity
- Name: CLAIMS_EXPERT
- Port: 8004
- Owner: Claims Dev
- Category: Business Reasoning

## Exact Responsibility
Claims Expert is the reasoning engine of BIAS.
It reconciles OCR data against authorization records
and produces the Master Summary that drives decisions.

## What This Service Does
1. Receives audit requests from Orchestrator
2. Fetches OCR text from File Management
3. Fetches authorization records from DB Agent
4. Fetches member claim history from DB Agent
5. Calls LLM Agent to summarize each document
6. Calls LLM Agent to reconcile OCR vs authorization
7. Detects discrepancies and assigns severity
8. Generates Master Summary with decision
9. Stores report in object storage
10. Returns audit_id immediately (202 pattern)
11. Hands off to Chatbot via Flight Plan on completion

## What This Service Must NEVER Do
- Call LLM providers directly (always via LLM Agent)
- Access databases directly (always via DB Agent)
- Store claim data permanently (use object storage for reports)
- Return PII in API responses
- Make final approval decisions without reconciliation data

## API Endpoints to Implement
- POST /api/v1/audit
- GET  /api/v1/audit/status/{audit_id}
- GET  /api/v1/summary/{claim_id}
- POST /api/v1/validate/policy
- GET  /health

## Decision Logic
- APPROVED: within_policy=true AND discrepancies=none or LOW only
- PENDING_REVIEW: within_policy=true AND discrepancies=MEDIUM
- REJECTED: within_policy=false OR discrepancies=HIGH

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use execute_hand_off from shared.communication_layer.hand_off
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, AcceptedResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
