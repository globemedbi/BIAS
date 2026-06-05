# Orchestrator Service — Claude Code Skill File

## Identity
- Name: ORCHESTRATOR
- Port: 8001
- Owner: Lead Architect
- Category: Brain / Control Tower

## Exact Responsibility
The Orchestrator is a pure logic engine.
It creates Flight Plans and manages service health.
It holds NO business logic and NO claim data.

## What This Service Does
1. Receives plan creation requests from Communicator
2. Selects correct business template based on request_type
3. Queries service registry for healthy service addresses
4. Injects addresses into Flight Plan steps
5. Persists Flight Plan via DB Agent
6. Runs health probes on all services every 30 seconds
7. Handles Stage 99 recovery requests
8. Exposes system metrics for BI dashboard

## What This Service Must NEVER Do
- Process or inspect claim document content
- Hold claim state in memory (always persist via DB Agent)
- Make direct database calls (always via DB Agent)
- Call LLM Agent directly
- Hardcode any service URL

## API Endpoints to Implement
- POST /plan/create
- POST /plan/{plan_id}/stage/update
- GET  /plan/{plan_id}/status
- POST /plan/{plan_id}/recover
- POST /registry/register
- GET  /registry
- GET  /metrics
- GET  /health

## Services This Service Calls
- DB Agent: persist/load Flight Plans, write audit logs, save registry
- All services: GET /health for health probes

## Services That Call This Service
- Communicator: POST /plan/create
- Any service: POST /plan/{id}/stage/update (stage commits)
- Any service: POST /plan/{id}/recover (Stage 99)

## Flight Plan Handling
- Read flight_plan_v1.json schema before building any plan
- Always populate service_registry from live registry (not hardcoded)
- Always persist plan to DB Agent before returning to Communicator
- Recovery logic lives in health_monitor/monitor.py

## Error Handling
- Every exception must be logged via DB Agent /logs/audit
- Every recovery attempt must update Flight Plan overall_status
- Health probe failures must update registry status immediately

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, ErrorResponse from shared.models.response
- All functions must have type hints
- All functions must have docstrings
- Minimum 80% test coverage
