"""
DB Agent — Service Registry routes.
Persists and loads the Orchestrator's service registry via the logging PostgreSQL database.
The registry maps service names to their live URLs and is rebuilt at Orchestrator startup.
"""

# type hints
from typing import Any, Dict, Optional

# FastAPI tools
from fastapi import APIRouter, HTTPException, Header

# Pydantic for request body validation
from pydantic import BaseModel

# the singleton DBAgent — validates tokens and dispatches operations
from agent.db_agent import db_agent

# shared structured logger
from shared.communication_layer.logger import get_logger

# mandatory BIAS response envelope
from shared.models.response import SuccessResponse

# creates the logger instance tagged "DB_AGENT"
logger = get_logger("DB_AGENT")

# creates the router — mounted in main.py under /registry
router = APIRouter()


# ── REQUEST MODEL ─────────────────────────────────────────────────────────────

class RegistrySaveRequest(BaseModel):
    """Request body for POST /registry/save — sent by the Orchestrator."""

    # a dict mapping each service name to its URL
    # example: { "claims-expert": "http://claims-expert:8004", ... }
    registry: Dict[str, Any]


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

# registers this function as the handler for POST /registry/save
@router.post("/save", summary="Persist the Orchestrator service registry")
async def save_registry(
    # FastAPI validates the request body — registry dict is required
    body: RegistrySaveRequest,
    # reads the X-Service-Token header from the HTTP request
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header to identify the caller
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Saves a snapshot of the Orchestrator's live service registry to the logging database.
    Called by the Orchestrator after every service registration change.
    The snapshot is used to restore the registry after a restart.
    """

    # log the save request — include how many services are in the registry snapshot
    logger.info(
        "registry_save_requested",
        from_service=x_service_name,
        service_count=len(body.registry),
    )

    # wrap in try/except to convert database errors into HTTP responses
    try:

        # route through token validation then to the save_registry handler
        result = await db_agent.handle(
            # maps to _handle_save_registry in agent/router.py
            route="save_registry",
            # pass the registry dict nested inside the payload
            payload=body.model_dump(),
            # the auth token from the header
            token=x_service_token or "",
            # the calling service name
            service_name=x_service_name or "unknown",
        )

    # bad or missing service token
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

    # unknown route name
    except KeyError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # PostgreSQL write failure or any unexpected error
    except Exception as exc:
        logger.error("registry_save_failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Registry save failed")

    # return a confirmation with the count of services that were persisted
    return SuccessResponse(service="DB_AGENT", data=result)


# registers this function as the handler for GET /registry/load
@router.get("/load", summary="Load the latest persisted service registry")
async def load_registry(
    # GET requests have no body — auth is still required via headers
    x_service_token: Optional[str] = Header(None),
    # reads the calling service name from the header
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Loads the most recently saved service registry snapshot from the logging database.
    Called by the Orchestrator on startup to restore its service registry without
    requiring every service to re-register from scratch.
    Returns an empty registry dict if no snapshot has been saved yet.
    """

    # log the load request
    logger.info("registry_load_requested", from_service=x_service_name)

    # wrap in try/except to convert failures into HTTP responses
    try:

        # route through token validation then to the load_registry handler
        result = await db_agent.handle(
            # maps to _handle_load_registry in agent/router.py
            route="load_registry",
            # GET has no body — pass an empty dict as the payload
            payload={},
            # the auth token from the header
            token=x_service_token or "",
            # the calling service name
            service_name=x_service_name or "unknown",
        )

    # bad or missing service token
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

    # unknown route name
    except KeyError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # PostgreSQL read failure or any unexpected error
    except Exception as exc:
        logger.error("registry_load_failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Registry load failed")

    # return the registry snapshot inside the standard response envelope
    return SuccessResponse(service="DB_AGENT", data=result)
