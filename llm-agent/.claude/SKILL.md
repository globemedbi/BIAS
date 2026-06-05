# LLM Agent Service — Claude Code Skill File

## Identity
- Name: LLM_AGENT
- Port: 8005
- Owner: AI Dev
- Category: AI Domain

## Exact Responsibility
The LLM Agent is the ONLY service that holds LLM API keys.
All LLM interactions in BIAS go through this service.
It abstracts providers and governs token usage.

## What This Service Does
1. Receives completion requests from Claims Expert and Chatbot
2. Selects appropriate model based on task_type and preference
3. Sanitizes prompts before sending to any external provider
4. Wraps requests in standardized system prompts per task_type
5. Validates response against expected schema
6. Retries with correction prompt if response malformed
7. Caches common responses to reduce cost
8. Tracks and reports token usage per calling service
9. Falls back to secondary provider on primary failure

## What This Service Must NEVER Do
- Share LLM API keys with any other service
- Accept raw prompts from external (internet-facing) sources
- Skip prompt sanitization (injection defense)
- Allow a single service to exceed token budget
- Log prompt content that contains PII

## API Endpoints to Implement
- POST /api/v1/complete
- POST /api/v1/embed
- GET  /api/v1/models
- GET  /api/v1/usage/report
- GET  /health

## Model Routing Rules
- FAST → DEFAULT_MODEL_FAST from env (simple tasks)
- BALANCED → DEFAULT_MODEL_BALANCED from env (standard tasks)
- POWERFUL → DEFAULT_MODEL_POWERFUL from env (complex reasoning)
- task_type overrides model_preference if conflict

## System Prompt Templates
Located in prompt_engine/templates/:
- summarize.txt → document summarization
- audit.txt → claims reconciliation
- reconcile.txt → data matching
- chat.txt → conversational responses
- extract.txt → entity extraction

## Provider Fallback Order
1. Primary: configured by DEFAULT_MODEL_* env vars
2. Fallback: next provider in router.py fallback chain
3. If all fail: return 503 with ALL_PROVIDERS_UNAVAILABLE

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, ErrorResponse from shared.models.response
- API keys ONLY loaded from environment variables
- Never log API keys even partially
- All functions must have type hints and docstrings
- Minimum 80% test coverage
