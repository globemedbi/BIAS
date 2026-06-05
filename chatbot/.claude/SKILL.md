# Chatbot Service — Claude Code Skill File

## Identity
- Name: CHATBOT
- Port: 8006
- Owner: Frontend Dev
- Category: User Interface

## Exact Responsibility
Chatbot is the conversational interface for all users.
It formats technical results into human language
and handles real-time user queries.

## What This Service Does
1. Receives formatted audit result from Claims Expert
2. Calls LLM Agent to adapt tone to user_type
3. Formats discrepancies as readable list
4. Triggers callback to Communicator with final result
5. Handles real-time chat messages from users
6. Classifies user intent via LLM Agent
7. Routes intent to correct service for data
8. Enforces user-level authorization on all data
9. Manages conversation sessions

## What This Service Must NEVER Do
- Display un-anonymized PII to any user
- Allow a MEMBER user to see another member's data
- Call databases directly (always via DB Agent)
- Call LLM providers directly (always via LLM Agent)
- Store conversation history permanently without TTL

## API Endpoints to Implement
- POST /api/v1/format
- POST /api/v1/chat
- GET  /api/v1/chat/history/{session_id}
- POST /api/v1/chat/session
- GET  /health

## Intent Classification Map
- STATUS_CHECK → Orchestrator /plan/{id}/status
- HISTORY_QUERY → DB Agent /claims/history
- POLICY_QUERY → Claims Expert /validate/policy
- DOCUMENT_REQUEST → File Management /extract/{claim_id}
- GENERAL_QUESTION → LLM Agent /complete (no data fetch)

## Tone Rules per user_type
- ADJUSTER: technical detail, include discrepancy codes, amounts
- MEMBER: plain language, no codes, focus on outcome and next steps
- ADMIN: full detail, include all metadata and audit trail

## Session Management
- In-memory dict for Phase 1
- Key: session_id, Value: {user_id, user_type, messages, context}
- TTL: SESSION_TTL_HOURS from environment
- Never log message content that contains PII

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use execute_hand_off from shared.communication_layer.hand_off
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, SuccessResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
