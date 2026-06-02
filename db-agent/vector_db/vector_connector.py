"""
Vector & JSON Procedure DB connector — Oracle 23ai, schema: mldsdev.

Pool strategy: one pool per unique (host, port, service, user) combination.
Pools are created lazily on first use and cached for the lifetime of the process.
This allows each YAML route to target a different Oracle server or schema
without restarting the service.
"""
import array
import asyncio
import json
import os
from typing import Any, Dict, List, Optional

import oracledb

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

# ── THICK MODE ────────────────────────────────────────────────────────────────
# Required for this Oracle 23ai server — thin mode fails with bytearray errors
# on Windows ProactorEventLoop.
oracledb.init_oracle_client()

# ── PER-ROUTE POOL CACHE ──────────────────────────────────────────────────────
# Key: "{user}@{host}:{port}/{service}"  → oracledb.ConnectionPool
# Built lazily on first use so the service starts even if a DB is unreachable.
_pool_cache: Dict[str, Any] = {}


def _build_dsn(host: str, port: int, service: str) -> str:
    """Assembles an Oracle TNS connect string from individual components."""
    return (
        f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))"
        f"(CONNECT_DATA=(SERVICE_NAME={service})))"
    )


def _get_pool(host: str, port: int, service: str, user: str, password: str):
    """
    Returns a cached pool for the given connection target, creating it if needed.
    Password is never stored in the cache key — only the connection coordinates.
    """
    # cache key uniquely identifies the (server, schema) combination
    cache_key = f"{user}@{host}:{port}/{service}"

    if cache_key not in _pool_cache:
        dsn  = _build_dsn(host, port, service)
        pool = oracledb.create_pool(
            user=user,
            password=password,
            dsn=dsn,
            min=int(os.getenv("VECTOR_DB_POOL_MIN", "2")),
            max=int(os.getenv("VECTOR_DB_POOL_SIZE", "5")),
            increment=1,
        )
        logger.info("oracle_pool_created", host=host, port=port, schema=user)
        _pool_cache[cache_key] = pool

    return _pool_cache[cache_key]


def _resolve_pool(db_conn: Optional[Dict] = None):
    """
    Selects or creates the correct pool for a request.

    If the YAML route has a 'database_connection' block, its host/port/service/schema
    override the env-var defaults — allowing each route to target a different server.
    The password is always read from VECTOR_DB_PASSWORD (never stored in YAML).

    db_conn example (from YAML):
        host: 192.168.244.198
        port: 1528
        service: aidev_pdb1.drdb.drdatabase.oraclevcn.com
        schema: mldsdev
    """
    # read env-var defaults — used when a field is absent from the YAML block
    default_host     = os.getenv("VECTOR_DB_HOST",     "")
    default_port     = int(os.getenv("VECTOR_DB_PORT", "1521"))
    default_service  = os.getenv("VECTOR_DB_SERVICE",  "")
    default_user     = os.getenv("VECTOR_DB_USER",     "")
    password         = os.getenv("VECTOR_DB_PASSWORD", "")  # always from env

    if db_conn:
        # per-route overrides from the YAML database_connection block
        host    = str(db_conn.get("host",    default_host))
        port    = int(db_conn.get("port",    default_port))
        service = str(db_conn.get("service", default_service))
        user    = str(db_conn.get("schema",  default_user))   # Oracle: schema == user
    else:
        # no YAML override — use env-var defaults (backwards compatible)
        host, port, service, user = default_host, default_port, default_service, default_user

    return _get_pool(host, port, service, user, password)


# ── VECTOR HELPERS ────────────────────────────────────────────────────────────

def _to_vec(values: List[float]) -> array.array:
    """Converts a Python float list to an Oracle VECTOR-compatible array."""
    return array.array("f", values)


# ── SYNC CALL IMPLEMENTATIONS ─────────────────────────────────────────────────
# These run in a thread executor so the asyncio event loop never blocks.

def _search_sync(vec: array.array, top_k: int, pool) -> List[Dict[str, Any]]:
    """Cosine ANN search against mldsdev.document_vectors."""
    sql = """
        SELECT doc_id,
               payload,
               VECTOR_DISTANCE(embedding, :query_vec, COSINE) AS distance
        FROM   mldsdev.document_vectors
        ORDER  BY VECTOR_DISTANCE(embedding, :query_vec, COSINE)
        FETCH  FIRST :top_k ROWS ONLY
    """
    results = []
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, query_vec=vec, top_k=top_k)
            for doc_id, payload_raw, distance in cur.fetchall():
                payload = (
                    json.loads(payload_raw)
                    if isinstance(payload_raw, str) else payload_raw
                )
                results.append({
                    "doc_id":  doc_id,
                    "score":   1.0 - distance,
                    "payload": payload,
                })
    return results


def _execute_json_procedure_sync(
    procedure_name: str,
    payload: Dict[str, Any],
    pool,
) -> Dict[str, Any]:
    """
    Calls a procedure with signature: (p_json_payload IN CLOB, p_json_response OUT CLOB).
    Serialises the payload dict to JSON, calls the procedure, parses the OUT CLOB response.
    call_type: json_clob
    """
    # normalize all top-level keys to lowercase so Oracle JSON_VALUE('$.claim_id')
    # matches regardless of whether the caller sent 'claim_id', 'CLAIM_ID', or 'Claim_Id'
    payload = {k.lower(): v for k, v in payload.items()}
    json_payload_str = json.dumps(payload)

    with pool.acquire() as conn:
        with conn.cursor() as cur:
            # bind an OUT CLOB variable to capture the procedure's JSON response
            out_response = cur.var(oracledb.DB_TYPE_CLOB)

            cur.callproc(procedure_name, [json_payload_str, out_response])

            # read the CLOB locator — returns None if the procedure returned nothing
            response_lob = out_response.getvalue()
            response_str = response_lob.read() if response_lob else "{}"
            return json.loads(response_str)


def _execute_named_procedure_sync(
    procedure_name: str,
    payload: Dict[str, Any],
    param_keys: List[str],
    pool,
) -> Dict[str, Any]:
    """
    Calls a procedure with individual typed IN parameters and no OUT CLOB.
    Extracts values from the payload dict in the order declared by param_keys.
    call_type: named_params
    """
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            # normalize keys to lowercase before extracting positional params
            payload = {k.lower(): v for k, v in payload.items()}
            params  = [payload.get(k) for k in param_keys]

            cur.callproc(procedure_name, params)

            # explicit commit for DML procedures that do not commit internally
            conn.commit()

    return {"status": "SUCCESS", "message": "Procedure executed successfully."}


# ── ASYNC CONNECTOR CLASS ─────────────────────────────────────────────────────

class VectorDBConnector:
    """
    Async interface to Oracle 23ai.
    All methods accept an optional db_conn dict (from the YAML database_connection block).
    When db_conn is None the env-var defaults are used — fully backwards compatible.
    """

    async def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        db_conn: Optional[Dict] = None,
    ) -> List[Dict[str, Any]]:
        """Cosine ANN search. Targets the pool resolved from db_conn (or env defaults)."""
        pool = _resolve_pool(db_conn)
        vec  = _to_vec(query_vector)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, _search_sync, vec, top_k, pool)
        logger.info("vector_search_done", top_k=top_k, returned=len(results))
        return results

    async def execute_procedure(
        self,
        procedure_name: str,
        payload: Dict[str, Any],
        db_conn: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Executes a json_clob procedure (IN CLOB JSON → OUT CLOB JSON).
        Routes to the pool specified by db_conn, or the default pool if None.
        """
        pool = _resolve_pool(db_conn)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None, _execute_json_procedure_sync, procedure_name, payload, pool
        )
        logger.info("procedure_executed", target=procedure_name)
        return results

    async def execute_named_procedure(
        self,
        procedure_name: str,
        payload: Dict[str, Any],
        param_keys: List[str],
        db_conn: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Executes a named_params procedure (individual typed IN args, no OUT CLOB).
        Routes to the pool specified by db_conn, or the default pool if None.
        """
        pool = _resolve_pool(db_conn)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None, _execute_named_procedure_sync, procedure_name, payload, param_keys, pool
        )
        logger.info("named_procedure_executed", target=procedure_name)
        return results
