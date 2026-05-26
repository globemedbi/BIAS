# Orchestrator Service

**Port:** 8001 | **Owner:** Lead Architect | **Category:** Brain / Control Tower

## Responsibility
Creates Flight Plans from business templates and manages service health.
Holds no business logic and no claim data.

## Key Files
- `agent/orchestrator_agent.py` — Flight Plan creation
- `service_registry/registry.py` — Live service URL tracking
- `health_monitor/monitor.py` — 30-second health probes
- `flight_plan/templates/` — Business process templates

## Running Locally
```bash
cd orchestrator
pip install -r requirements.txt
uvicorn api.main:app --port 8001 --reload
```

## Testing
```bash
pytest --cov=. --cov-fail-under=80
```

## API
See `docs/api-contracts/orchestrator.md`
