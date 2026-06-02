"""
DB Agent Route Registry.

Adding a new database operation requires three steps:
  1. Write a handler function: async def _handle_<name>(payload) -> dict
  2. Register it in ROUTE_REGISTRY with a string key
  3. Add the matching HTTP endpoint in the relevant routes file
Nothing else needs to change.
"""

# type hints for the handler signature and registry dictionary
from typing import Any, Callable, Dict, List

# Oracle 23ai stored procedure executor — used for the claims attachment flow
from oracle_db.oracle_connector import call_procedure

# PostgreSQL connectors for legacy data, logging, and DWH
from legacy_db.legacy_connector import LegacyDBConnector
from logging_db.logging_connector import LoggingDBConnector
from dwh.dwh_connector import DWHConnector

# Oracle 23ai vector search connector — used for the VECTOR target_db path
from vector_db.vector_connector import VectorDBConnector

# NL2SQL translator — converts natural language to validated SQL via LLM Agent
from nl2sql.translator import translate as nl_translate

# routing registry — used by the pkg_procedure: dispatcher to read call_type
from agent.routing_registry import lookup, get_required_input_keys

# shared structured logger
from shared.communication_layer.logger import get_logger

# creates the logger tagged "DB_AGENT"
logger = get_logger("DB_AGENT")

# type alias: a RouteHandler is any async callable that takes a dict and returns a value
RouteHandler = Callable[[Dict[str, Any]], Any]

# connector singletons — one instance each, shared across all requests
_legacy = LegacyDBConnector()
_logging = LoggingDBConnector()
_dwh = DWHConnector()
_vector = VectorDBConnector()


# ── HANDLERS — one async function per supported database operation ─────────────

async def _handle_process_attachment(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Calls the Oracle stored procedure that processes a claim attachment JSON."""

    # delegates to oracle_connector.call_procedure with the fully-qualified procedure name
    return await call_procedure(
        # the Oracle package + procedure name to call
        "PKG_AGENT_INSERT_CLAIM.PROCESS_ATTACHMENT_JSON",
        # the claim attachment data to pass as the IN CLOB parameter
        payload,
    )


async def _handle_fetch_authorization(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Fetches authorization and coverage data for a claim from the legacy PostgreSQL DB."""

    # extract claim_id from the payload — required field, validated by the route model
    claim_id = payload["claim_id"]

    # call the legacy connector — returns None if no authorization record exists
    result = await _legacy.fetch_authorization(claim_id)

    # if no record was found, return a structured "not found" response rather than crashing
    if result is None:
        return {"found": False, "claim_id": claim_id}

    # merge the found flag into the result dict before returning
    return {"found": True, **result}


async def _handle_fetch_member_history(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Returns all historical claims for a member from the legacy PostgreSQL DB."""

    # extract member_id from the payload — required field
    member_id = payload["member_id"]

    # fetch the full claim history list (may be empty if the member has no claims)
    history = await _legacy.fetch_member_history(member_id)

    # wrap the list in a dict so the response shape is consistent with other handlers
    return {"member_id": member_id, "count": len(history), "claims": history}


async def _handle_write_audit_log(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Writes one audit event to the logging PostgreSQL database."""

    # pass the entire payload dict to the logging connector — it extracts fields internally
    success = await _logging.write_audit_event(payload)

    # return a simple acknowledgement dict — no data to echo back
    return {"written": success}


async def _handle_nl_query(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Translates a natural language question to SQL and executes it on the target database."""

    # extract the English question from the payload
    query = payload["query"]

    # extract the target database — must be one of LEGACY, DWH, VECTOR
    target_db = payload.get("target_db", "LEGACY").upper()

    # VECTOR path: use semantic similarity search instead of SQL
    if target_db == "VECTOR":

        # query_vector must be provided by the caller for vector searches
        query_vector: List[float] = payload.get("query_vector", [])

        # if no vector was provided, we cannot perform vector search
        if not query_vector:
            return {"error": "query_vector required for VECTOR target_db"}

        # call the Oracle 23ai vector search function
        results = await _vector.search(query_vector, top_k=payload.get("top_k", 5))

        # return results in a consistent wrapper
        return {"target_db": "VECTOR", "results": results}

    # call the NL2SQL translator — sends the English query to LLM Agent
    sql = await nl_translate(query)

    # if translation failed (LLM Agent unreachable or unsafe SQL), return an error dict
    if sql is None:
        return {"error": "Could not translate query to SQL — LLM Agent may be unavailable"}

    # LEGACY path: execute the validated SQL on the on-premise PostgreSQL database
    if target_db == "LEGACY":

        # use the legacy connector's raw query method — it receives pre-validated SQL
        results = await _legacy.execute_query_raw(sql)

    # DWH path: execute on the data warehouse PostgreSQL database
    elif target_db == "DWH":

        # use the DWH connector — read-only, analytics database
        results = await _dwh.execute_query(sql)

    # unknown target_db value — should have been caught by route validation, but guard anyway
    else:
        return {"error": f"Unknown target_db: {target_db}"}

    # return the SQL that was executed alongside the results for transparency
    return {"target_db": target_db, "sql": sql, "results": results}


async def _handle_save_registry(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Persists the Orchestrator's service registry to the logging database."""

    # the registry is a dict of { service_name: url } pairs
    registry = payload.get("registry", {})

    # write the registry snapshot to the logging DB
    success = await _logging.write_registry(registry)

    # return a confirmation with the count of services that were saved
    return {"saved": success, "service_count": len(registry)}


async def _handle_load_registry(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Loads the most recently saved service registry from the logging database."""

    # load the latest registry snapshot — returns {} if nothing has been saved yet
    registry = await _logging.load_registry()

    # wrap in a standard response dict
    return {"registry": registry, "service_count": len(registry)}


# ── REGISTRY — maps every route string to its handler function ────────────────

ROUTE_REGISTRY: Dict[str, RouteHandler] = {
    # Oracle 23ai stored procedure — claim attachment processing
    "process_attachment":   _handle_process_attachment,

    # Legacy PostgreSQL — authorization and coverage lookup
    "fetch_authorization":  _handle_fetch_authorization,

    # Legacy PostgreSQL — member claim history
    "fetch_member_history": _handle_fetch_member_history,

    # Logging PostgreSQL — audit event write
    "write_audit_log":      _handle_write_audit_log,

    # NL2SQL — natural language to SQL via LLM Agent, then execute on target DB
    "nl_query":             _handle_nl_query,

    # Logging PostgreSQL — persist Orchestrator service registry
    "save_registry":        _handle_save_registry,

    # Logging PostgreSQL — load latest service registry snapshot
    "load_registry":        _handle_load_registry,
}


# ── DISPATCHER — the single public function all route files call ──────────────

async def dispatch(route: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Looks up the route and calls its handler. Raises KeyError for unknown routes."""

    # ── GENERIC ORACLE PROCEDURE PREFIX ──────────────────────────────────────────
    # any route that starts with "pkg_procedure:" is a direct Oracle stored-procedure
    # call — the procedure name is everything after the colon, e.g.:
    #   "pkg_procedure:PKG_AGENT_INSERT_CLAIM.PROCESS_ATTACHMENT_JSON"
    # this avoids having to register every Oracle procedure explicitly in ROUTE_REGISTRY
    if route.startswith("pkg_procedure:"):

        # strip the prefix to get the fully-qualified Oracle procedure name
        procedure_name = route[len("pkg_procedure:"):]

        # guard: procedure name must not be blank after stripping the prefix
        if not procedure_name:
            raise KeyError("pkg_procedure: route requires a procedure name after the colon")

        # read the registry entry to determine which call path to use
        entry     = lookup(route)
        call_type = entry.get("call_type", "json_clob") if entry else "json_clob"

        logger.info("dispatching_procedure", procedure=procedure_name, call_type=call_type)

        if call_type == "named_params":
            # procedure has individual typed IN params and no OUT CLOB
            # use input_keys from the registry to build the positional argument list
            param_keys = get_required_input_keys(route)
            return await _vector.execute_named_procedure(procedure_name, payload, param_keys)

        # default: procedure expects (IN CLOB JSON, OUT CLOB JSON)
        return await _vector.execute_procedure(procedure_name, payload)

    # ── STATIC REGISTRY LOOKUP ────────────────────────────────────────────────────

    # look up the handler by name — returns None if not registered
    handler = ROUTE_REGISTRY.get(route)

    # if the route name is not in the registry, reject it immediately
    if handler is None:
        # log the unknown route name so developers can debug missing registrations
        logger.warning("unknown_route", route=route)
        # the calling route file catches KeyError and converts it to HTTP 422
        raise KeyError(f"Unknown route: '{route}'")

    # log which operation is being executed — useful for distributed tracing
    logger.info("dispatching", route=route)

    # call the handler and return its result — all handlers are async
    return await handler(payload)
