# Communicator Service

**Port:** 8000 | **Owner:** Backend Dev | **Category:** External Gateway

## Responsibility
The ONLY externally-exposed service. Validates, packages, routes. Nothing more.

## Key Files
- `auth/jwt_validator.py` — JWT validation
- `routing/request_router.py` — Calls Orchestrator
- `agent/communicator_agent.py` — Session management

## Running Locally
```bash
cd communicator
pip install -r requirements.txt
uvicorn api.main:app --port 8000 --reload
```

## API
See `docs/api-contracts/communicator.md`
