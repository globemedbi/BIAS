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

# routing registry — used by the dispatcher to read connector, call_type, sql, input_keys
from agent.routing_registry import (
    lookup, get_required_input_keys, get_connector, get_sql, get_database_connection
)

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
    """
    YAML-driven dispatcher.

    Resolution order:
      1. Read 'connector' and 'call_type' from routing_registry.yaml
      2. Route to the correct DB connector based on those two fields
      3. Fall through to static ROUTE_REGISTRY for complex routes that
         need custom Python logic (nl_query, fetch_authorization, etc.)

    connector values → DB connector
        oracle           → VectorDBConnector  (Oracle 23ai)
        legacy_postgres  → LegacyDBConnector  (on-premise PostgreSQL)
        dwh              → DWHConnector        (data-warehouse PostgreSQL)
        logging_postgres → LoggingDBConnector  (logging PostgreSQL)

    call_type values → how to call the connector
        json_clob    → Oracle: callproc(IN CLOB JSON, OUT CLOB JSON)
        named_params → Oracle: callproc with individual typed IN params
        sql_select   → PostgreSQL: parameterised SELECT, returns rows
        sql_dml      → PostgreSQL: parameterised INSERT/UPDATE/DELETE
    """

    # ── STEP 1: READ YAML METADATA ────────────────────────────────────────────

    entry = lookup(route)

    if entry:
        connector = get_connector(route)   # which DB to target
        call_type = entry.get("call_type", "json_clob")

        logger.info("dispatching", route=route, connector=connector, call_type=call_type)

        # ── ORACLE CONNECTOR ──────────────────────────────────────────────────
        if connector == "oracle":

            # ── PROCEDURE NAME ────────────────────────────────────────────────
            # Resolution order:
            #   1. package + procedure from YAML → "PKG_NAME.PROC_NAME"
            #   2. procedure field alone (if already fully qualified)
            #   3. strip the pkg_procedure: prefix from the route key (fallback)
            pkg  = str(entry.get("package")   or "").strip()
            proc = str(entry.get("procedure") or "").strip()
            if pkg and proc:
                procedure_name = f"{pkg}.{proc}"
            elif proc:
                procedure_name = proc
            elif route.startswith("pkg_procedure:"):
                procedure_name = route[len("pkg_procedure:"):]
            else:
                procedure_name = route

            if not procedure_name:
                raise KeyError(f"Route '{route}' has connector=oracle but no procedure name")

            # ── DATABASE CONNECTION ───────────────────────────────────────────
            # Read the per-route database_connection block from the YAML.
            # If absent, the connector falls back to VECTOR_DB_* env-var defaults.
            # This is what allows each route to target a different Oracle server.
            db_conn = get_database_connection(route)

            if call_type == "named_params":
                param_keys = get_required_input_keys(route)
                return await _vector.execute_named_procedure(
                    procedure_name, payload, param_keys, db_conn
                )

            # default: json_clob — (IN CLOB JSON, OUT CLOB JSON)
            return await _vector.execute_procedure(procedure_name, payload, db_conn)

        # ── POSTGRESQL CONNECTORS ─────────────────────────────────────────────
        if connector in ("legacy_postgres", "dwh", "logging_postgres"):

            # select the correct asyncpg connector instance
            pg_connector = {
                "legacy_postgres":  _legacy,
                "dwh":              _dwh,
                "logging_postgres": _logging,
            }[connector]

            # read the SQL template from the YAML 'sql:' field
            sql = get_sql(route)
            if not sql:
                raise KeyError(
                    f"Route '{route}' has connector={connector} but no 'sql:' field in YAML"
                )

            # build the ordered parameter list from input_keys
            param_keys = get_required_input_keys(route)
            params     = [payload.get(k) for k in param_keys]

            if call_type == "sql_dml":
                # INSERT / UPDATE / DELETE — commit is handled by the connector
                await pg_connector.execute_query_raw(sql, params)
                return {"status": "SUCCESS", "affected_rows": 1}

            # default PostgreSQL call type: sql_select — returns rows as list of dicts
            rows = await pg_connector.execute_query_raw(sql, params)
            return {"rows": rows, "count": len(rows)}

    # ── STEP 2: STATIC ROUTE REGISTRY (complex / custom-logic routes) ─────────
    # Routes that need Python logic beyond a single SQL/procedure call
    # (e.g. nl_query invokes LLM Agent; fetch_authorization reshapes the result).
    # These stay here until they are simple enough to express in the YAML.

    handler = ROUTE_REGISTRY.get(route)

    if handler is None:
        logger.warning("unknown_route", route=route)
        raise KeyError(f"Unknown route: '{route}'")

    logger.info("dispatching_static", route=route)
    return await handler(payload)
