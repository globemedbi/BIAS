"""
DB Agent — Audit log routes.
Receives audit events from all BIAS services and writes them to the logging PostgreSQL database.
"""

# type hint for optional headers
from typing import Optional

# FastAPI tools
from fastapi import APIRouter, HTTPException, Header

# Pydantic for request body validation
from pydantic import BaseModel

# the singleton DBAgent — validates token and dispatches to the correct handler
from agent.db_agent import db_agent

# shared structured logger
from shared.communication_layer.logger import get_logger

# mandatory BIAS response envelope
from shared.models.response import SuccessResponse

# creates the logger instance tagged "DB_AGENT"
logger = get_logger("DB_AGENT")

# creates the router — mounted in main.py under /logs
router = APIRouter()


# ── REQUEST MODEL ─────────────────────────────────────────────────────────────

class AuditLogRequest(BaseModel):
    """Request body for POST /logs/audit — sent by any BIAS service to record an event."""

    # the Flight Plan ID this event belongs to — links the log entry to a specific claim workflow
    plan_id: str

    # the stage number within the Flight Plan where this event occurred
    stage: int

    # the name of the service that is reporting this event (e.g. "CLAIMS_EXPERT")
    service: str

    # a machine-readable category for the event (e.g. "CLAIM_PROCESSED", "OCR_COMPLETE")
    event_type: str

    # a human-readable description of what happened
    message: str

    # an optional error code — present only on failure events, None on success events
    error_code: Optional[str] = None


# ── ENDPOINT ──────────────────────────────────────────────────────────────────

# registers this function as the handler for POST /logs/audit
@router.post("/audit", summary="Write an audit log entry to the logging database")
async def write_audit_log(
    # FastAPI parses and validates the request body into this typed object
    request: AuditLogRequest,
    # reads the X-Service-Token header from the HTTP request
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header to know which service is calling
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Receives an audit event from any BIAS service and writes it to the logging database.
    Called after every significant operation in the platform for SIEM and compliance.
    """

    # log the incoming write request — include plan_id so this log line is searchable
    logger.info(
        "audit_log_write_requested",
        from_service=x_service_name,
        plan_id=request.plan_id,
        event_type=request.event_type,
    )

    # wrap in try/except to convert database failures into HTTP error responses
    try:

        # route through token validation then to the logging connector handler
        result = await db_agent.handle(
            # maps to _handle_write_audit_log in agent/router.py
            route="write_audit_log",
            # convert the Pydantic model to a plain dict — handler passes it to LoggingDBConnector
            payload=request.model_dump(),
            # the service token (empty string if header was missing)
            token=x_service_token or "",
            # the reporting service's name (defaults to "unknown" if omitted)
            service_name=x_service_name or "unknown",
        )

    # bad or missing service token — db_agent raises PermissionError
    except PermissionError as exc:
        # HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail=str(exc))

    # unknown route name — should never happen but guarded defensively
    except KeyError as exc:
        # HTTP 422 Unprocessable Entity
        raise HTTPException(status_code=422, detail=str(exc))

    # database connectivity failure, constraint violation, or any other unexpected error
    except Exception as exc:
        # log internally — do not expose PostgreSQL error details to callers
        logger.error("audit_log_write_failed", error=str(exc))
        # HTTP 500 Internal Server Error
        raise HTTPException(status_code=500, detail="Audit log write failed")

    # return a success confirmation — callers do not need to see the DB row
    return SuccessResponse(service="DB_AGENT", data=result)
