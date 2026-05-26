# Chatbot Service

**Port:** 8006 | **Owner:** Frontend Dev | **Category:** User Interface

## Responsibility
Conversational interface for all users. Formats technical results into human language
and handles real-time queries. Enforces user-level data authorization.

## Key Files
- `nlu/intent_classifier.py` — User intent classification
- `conversation/session_manager.py` — In-memory session store with TTL
- `formatter/response_formatter.py` — Tone-adapted output per user_type
- `agent/chatbot_agent.py` — Format + callback to Communicator

## Tone Rules
- `MEMBER`: plain language, outcome focus, no codes
- `ADJUSTER`: technical detail, discrepancy codes, amounts
- `ADMIN`: full detail with audit trail

## Running Locally
```bash
cd chatbot
pip install -r requirements.txt
uvicorn api.main:app --port 8006 --reload
```

## API
See `docs/api-contracts/chatbot.md`
