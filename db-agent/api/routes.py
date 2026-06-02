"""
DB Agent — Generic Oracle Procedure API Layer (Layer 1).

Exposes a single POST /execute-procedure endpoint that accepts any Oracle
stored-procedure name and an arbitrary JSON payload. The procedure name is
forwarded to the router as a "pkg_procedure:<name>" route so that any Oracle
PL/SQL package/procedure can be called without touching this file.

Architecture:
  HTTP client → POST /execute-procedure
              → Layer 2  agent/agent.py      (token validation)
              → Layer 3  agent/router.py     (pkg_procedure: prefix dispatch)
              → Layer 4  vector_db/vector_connector.py  (Oracle callproc)
"""

# APIRouter groups these endpoints under a mountable prefix in main.py
from fastapi import APIRouter, HTTPException

# BaseModel turns a plain Python class into a JSON-schema-validated request body
from pydantic import BaseModel

# type hints for the arbitrary JSON payload
from typing import Dict, Any

# Layer 2: the security singleton — validates the service token before dispatching
from agent.agent import db_agent

# creates the router that main.py will mount under a URL prefix
router = APIRouter()


# ── REQUEST MODEL ─────────────────────────────────────────────────────────────

class DBProcedureRequest(BaseModel):
    """
    Request body for POST /execute-procedure.

    The caller specifies which Oracle procedure to run and supplies its input
    as a free-form JSON object. Authentication is carried inside the body
    (rather than headers) so the generic endpoint needs no header extraction.
    """

    # fully-qualified Oracle procedure name, e.g. "PKG_CLAIMS.GET_CLAIM_STATUS"
    # the router prepends "pkg_procedure:" before forwarding to the dispatch layer
    target_procedure: str

    # arbitrary key-value pairs that become the IN CLOB parameter sent to Oracle
    # the procedure is responsible for interpreting the contents
    payload: Dict[str, Any]

    # BIAS internal service token — compared against INTERNAL_SERVICE_TOKEN env var
    # in agent.db_agent.DBAgent.validate_service_token()
    token: str

    # name of the calling service, used only for logging ("claims-expert", etc.)
    service_name: str


# ── ENDPOINT ──────────────────────────────────────────────────────────────────

# registers this coroutine as the handler for POST /execute-procedure
@router.post("/execute-procedure", summary="Execute any Oracle stored procedure")
async def execute_oracle_procedure(req: DBProcedureRequest):
    """
    Generic entry point for calling any Oracle PL/SQL stored procedure.

    The procedure must accept a single IN CLOB (JSON string) and return a
    single OUT CLOB (JSON string).  The router constructs the canonical route
    key "pkg_procedure:<target_procedure>" so the dispatch layer knows to call
    VectorDBConnector.execute_procedure() directly without a static registry entry.

    Returns:
        {"status": "SUCCESS", "data": <procedure response dict>}
    """

    # wrap the entire dispatch chain in try/except so Oracle errors become HTTP
    # responses instead of unhandled 500s with raw Python tracebacks
    try:

        # Layer 2 (security) + Layer 3 (routing) in one call:
        # db_agent.handle() validates the token, then calls dispatch() which
        # detects the "pkg_procedure:" prefix and routes to VectorDBConnector
        result = await db_agent.handle(
            # the router prefix + procedure name — dispatch() strips the prefix
            route=f"pkg_procedure:{req.target_procedure}",
            # the arbitrary JSON payload forwarded as-is to the Oracle procedure
            payload=req.payload,
            # BIAS service token — validated in Layer 2 before any DB call happens
            token=req.token,
            # calling service name — recorded in the log entry
            service_name=req.service_name,
        )

        # return the standard BIAS success envelope expected by all callers
        return {"status": "SUCCESS", "data": result}

    # bad or missing INTERNAL_SERVICE_TOKEN — Layer 2 raises this
    except PermissionError as e:
        # 401 Unauthorized — do not include Oracle details in the message
        raise HTTPException(status_code=401, detail=str(e))

    # unknown route key or blank procedure name — Layer 3 raises this
    except KeyError as e:
        # 400 Bad Request — the procedure name was missing or malformed
        raise HTTPException(status_code=400, detail=str(e))

    # Oracle callproc error, network failure, or any other unexpected exception
    except Exception as e:
        # 500 Internal Server Error — include a generic message, not the raw Oracle error
        raise HTTPException(
            status_code=500,
            detail=f"Database execution failed: {str(e)}",
        )
