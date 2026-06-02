"""
DB Agent — Claims routes.
Handles claim attachment processing (Oracle) and member claim history (Legacy PostgreSQL).
"""

# type hint for optional HTTP headers
from typing import Optional

# FastAPI tools: router builder, HTTP exception raiser, header extractor
from fastapi import APIRouter, Header, HTTPException

# Pydantic BaseModel for request body validation
from pydantic import BaseModel

# the singleton DBAgent that validates tokens and routes operations
from agent.db_agent import db_agent

# shared structured logger tagged "DB_AGENT"
from shared.communication_layer.logger import get_logger

# mandatory BIAS response envelope
from shared.models.response import SuccessResponse

# creates the logger instance for this module
logger = get_logger("DB_AGENT")

# creates the FastAPI router — mounted in main.py under the /claims prefix
router = APIRouter()


# ── REQUEST MODELS ────────────────────────────────────────────────────────────

class AttachmentPayload(BaseModel):
    """Request body for POST /claims/store — sent by the Claims Expert after OCR."""

    # the unique identifier of the claim this attachment belongs to
    claim_id: str

    # the file name of the scanned document (e.g. "invoice_scan.pdf")
    attachment_name: str

    # the position of this attachment within the claim (1, 2, 3 ...)
    attachment_order: int

    # the document version number — incremented on re-submission
    version: int

    # how many pages were scanned in this document
    page_count: int

    # the full text extracted from the document by the OCR engine
    extracted_text: str


class ClaimHistoryRequest(BaseModel):
    """Request body for POST /claims/history — sent by the Chatbot or Claims Expert."""

    # the member whose full claim history is being requested
    # note: this is member_id, not claim_id — history is a member-level concept
    member_id: str


# ── ENDPOINTS ─────────────────────────────────────────────────────────────────

# registers this function as the handler for POST /claims/store
@router.post("/store", summary="Process a claim attachment via Oracle stored procedure")
async def store_claim(
    # FastAPI parses the JSON body and validates it against AttachmentPayload
    body: AttachmentPayload,
    # reads the X-Service-Token header — None if omitted
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header to identify the calling service
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Receives an attachment payload from an AI agent, calls
    PKG_AGENT_INSERT_CLAIM.PROCESS_ATTACHMENT_JSON on Oracle 23ai,
    and returns the procedure's JSON response.
    """

    # log the incoming request for audit traceability
    logger.info("claim_store_requested", from_service=x_service_name, claim_id=body.claim_id)

    # wrap the entire operation to convert Python exceptions to HTTP status codes
    try:

        # route the request through token validation then to the Oracle handler
        result = await db_agent.handle(
            # maps to _handle_process_attachment in agent/router.py
            route="process_attachment",
            # convert the Pydantic model to a plain dict for the Oracle call
            payload=body.model_dump(),
            # the service token from the header (empty string if missing)
            token=x_service_token or "",
            # the calling service name (defaults to "unknown" if header was omitted)
            service_name=x_service_name or "unknown",
        )

    # wrong or missing service token — agent rejects with PermissionError
    except PermissionError as exc:
        # HTTP 401 Unauthorized
        raise HTTPException(status_code=401, detail=str(exc))

    # unregistered route name — should not happen but guarded defensively
    except KeyError as exc:
        # HTTP 422 Unprocessable Entity
        raise HTTPException(status_code=422, detail=str(exc))

    # any other failure — Oracle error, network issue, unexpected exception
    except Exception as exc:
        # log the raw error internally for debugging
        logger.error("store_claim_failed", error=str(exc))
        # return a generic 500 — never expose raw Oracle error messages to callers
        raise HTTPException(status_code=500, detail="Oracle procedure execution failed")

    # wrap the Oracle procedure's JSON response in the standard BIAS envelope
    return SuccessResponse(service="DB_AGENT", data=result)


# registers this function as the handler for POST /claims/history
@router.post("/history", summary="Fetch all historical claims for a member")
async def get_claim_history(
    # FastAPI parses and validates the request body — member_id is required
    body: ClaimHistoryRequest,
    # reads the X-Service-Token header
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Returns all historical claims for a member from the legacy PostgreSQL database.
    Ordered newest first. Empty list if the member has no claim history.
    """

    # log the incoming request with the member ID for traceability
    logger.info("claim_history_requested", from_service=x_service_name, member_id=body.member_id)

    # wrap the database call to convert exceptions to HTTP responses
    try:

        # route through token validation then to the legacy PostgreSQL handler
        result = await db_agent.handle(
            # maps to _handle_fetch_member_history in agent/router.py
            route="fetch_member_history",
            # the member_id is the only field — pass as a dict
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

    # any other database or network failure
    except Exception as exc:
        logger.error("fetch_history_failed", error=str(exc))
        raise HTTPException(status_code=500, detail="Claim history fetch failed")

    # return the list of historical claims inside the standard response envelope
    return SuccessResponse(service="DB_AGENT", data=result)
