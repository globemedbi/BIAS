"""
DB Agent — Authorization routes.
Fetches authorization status and coverage records for a claim from the legacy PostgreSQL DB.
"""

# type hint for optional HTTP headers
from typing import Optional

# FastAPI tools: router builder, HTTP exception raiser, header extractor
from fastapi import APIRouter, HTTPException, Header

# Pydantic BaseModel for request body validation
from pydantic import BaseModel

# the singleton DBAgent instance that validates tokens and dispatches operations
from agent.db_agent import db_agent

# shared structured logger tagged "DB_AGENT"
from shared.communication_layer.logger import get_logger

# mandatory BIAS response envelope — all endpoints must return this shape
from shared.models.response import SuccessResponse

# creates the logger instance for this module
logger = get_logger("DB_AGENT")

# creates the FastAPI router — endpoints defined below are mounted in main.py under /authorization
router = APIRouter()


# ── REQUEST MODEL ─────────────────────────────────────────────────────────────

class AuthorizationRequest(BaseModel):
    """Request body for the /authorization/fetch endpoint."""

    # the unique claim identifier — Pydantic rejects the request if this field is missing or not a string
    claim_id: str


# ── ENDPOINT ──────────────────────────────────────────────────────────────────

# registers this function as the handler for POST /authorization/fetch
@router.post("/fetch", summary="Fetch authorization and coverage records for a claim")
async def fetch_authorization(
    # FastAPI reads the JSON request body and validates it against AuthorizationRequest
    body: AuthorizationRequest,
    # reads the X-Service-Token header — None if the caller omitted it
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header to identify which service is calling
    x_service_name: Optional[str] = Header(None),
# return type tells FastAPI to serialize the response using the SuccessResponse Pydantic model
) -> SuccessResponse:
    """
    Fetches authorization status and coverage details for a claim.
    Queries the legacy PostgreSQL database via the LegacyDBConnector.
    Returns the authorization record or a not-found indicator if no record exists.
    """

    # log the incoming request with the calling service name for the audit trail
    logger.info("authorization_fetch_requested", from_service=x_service_name, claim_id=body.claim_id)

    # wrap the database call in try/except to convert Python exceptions to HTTP responses
    try:

        # pass the request through the token-validation + dispatch chain
        result = await db_agent.handle(
            # the route name registered in agent/router.py ROUTE_REGISTRY
            route="fetch_authorization",
            # convert the Pydantic model to a plain dict for the handler
            payload=body.model_dump(),
            # pass the token (empty string if header was missing — agent will reject it)
            token=x_service_token or "",
            # pass the caller's service name (or "unknown" if header was omitted)
            service_name=x_service_name or "unknown",
        )

    # bad or missing service token — db_agent.handle raises PermissionError
    except PermissionError as exc:
        # converts to HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail=str(exc))

    # unknown route name — dispatch raises KeyError (should never happen here)
    except KeyError as exc:
        # converts to HTTP 422 Unprocessable Entity
        raise HTTPException(status_code=422, detail=str(exc))

    # any other error — database connectivity, query failure, etc.
    except Exception as exc:
        # log the full error message for debugging without exposing it to the caller
        logger.error("fetch_authorization_failed", error=str(exc))
        # return a generic 500 — never expose raw database errors to external callers
        raise HTTPException(status_code=500, detail="Authorization fetch failed")

    # wrap the result dict in the standard BIAS SuccessResponse envelope
    return SuccessResponse(service="DB_AGENT", data=result)
