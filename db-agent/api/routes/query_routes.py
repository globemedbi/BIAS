"""
DB Agent — NL2SQL query routes.
Accepts a natural language question, translates it to SQL via LLM Agent,
and executes it against the requested database (LEGACY, DWH, or VECTOR).
"""

# Literal restricts a field to a fixed set of allowed string values
from typing import Literal, Optional

# FastAPI tools
from fastapi import APIRouter, HTTPException, Header

# Pydantic for request body validation
from pydantic import BaseModel

# the singleton DBAgent — validates tokens and dispatches to the correct handler
from agent.db_agent import db_agent

# shared structured logger
from shared.communication_layer.logger import get_logger

# mandatory BIAS response envelope
from shared.models.response import SuccessResponse

# creates the logger instance tagged "DB_AGENT"
logger = get_logger("DB_AGENT")

# creates the router — mounted in main.py under /query
router = APIRouter()


# ── REQUEST MODEL ─────────────────────────────────────────────────────────────

class NLQueryRequest(BaseModel):
    """Request body for POST /query/nl."""

    # the natural language question to translate and execute
    # example: "Show me all approved claims from last month"
    query: str

    # which database to run the translated SQL against
    # Literal restricts the value — Pydantic rejects any string not in this set
    target_db: Literal["LEGACY", "DWH", "VECTOR"] = "LEGACY"

    # optional: pre-computed embedding vector for VECTOR target_db searches
    # callers must provide this when target_db is VECTOR
    query_vector: Optional[list] = None

    # how many vector search results to return — only relevant for VECTOR target_db
    top_k: int = 5


# ── ENDPOINT ──────────────────────────────────────────────────────────────────

# registers this function as the handler for POST /query/nl
@router.post("/nl", summary="Translate a natural language query to SQL and execute it")
async def natural_language_query(
    # FastAPI parses and validates the request body against NLQueryRequest
    request: NLQueryRequest,
    # reads the X-Service-Token header
    x_service_token: Optional[str] = Header(None),
    # reads the X-Service-Name header
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """
    Sends the natural language query to LLM Agent for SQL generation,
    validates the generated SQL is safe (SELECT-only, whitelisted tables),
    then executes it on the specified target database.

    Safety: all generated SQL passes through is_safe_query() before execution.
    Only SELECT statements are ever executed.
    """

    # log the request — record target_db but NOT the query text (may contain PII)
    logger.info(
        "nl_query_requested",
        from_service=x_service_name,
        target_db=request.target_db,
    )

    # wrap in try/except to convert all failures to proper HTTP responses
    try:

        # route through token validation then to the nl_query handler in router.py
        result = await db_agent.handle(
            # maps to _handle_nl_query in agent/router.py
            route="nl_query",
            # pass the full request as a dict — handler extracts query, target_db, query_vector, top_k
            payload=request.model_dump(),
            # the service token from the header
            token=x_service_token or "",
            # the calling service name
            service_name=x_service_name or "unknown",
        )

    # bad or missing service token
    except PermissionError as exc:
        raise HTTPException(status_code=401, detail=str(exc))

    # unknown route name (should never happen in production)
    except KeyError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # LLM Agent unreachable, database failure, or any unexpected error
    except Exception as exc:
        # log the error for debugging without exposing it to the caller
        logger.error("nl_query_failed", error=str(exc))
        # HTTP 500 — do not expose internal SQL or database errors
        raise HTTPException(status_code=500, detail="NL query execution failed")

    # if the handler returned an error key, surface it as HTTP 422 with the explanation
    if "error" in result:
        raise HTTPException(status_code=422, detail=result["error"])

    # return the query results inside the standard BIAS response envelope
    return SuccessResponse(service="DB_AGENT", data=result)
