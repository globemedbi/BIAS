"""
Vector & JSON Procedure DB connector — Oracle 23ai, schema: mldsdev.
"""
import array
import asyncio
import json
import os
from typing import Any, Dict, List

import oracledb

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

# ── Oracle 23ai connection ────────────────────────────────────────────────────
oracledb.init_oracle_client()   # thick mode — requires Oracle Instant Client

_DSN = os.getenv("VECTOR_DB_DSN", "")

_pool = oracledb.create_pool(
    user=os.getenv("VECTOR_DB_USER", ""),
    password=os.getenv("VECTOR_DB_PASSWORD", ""),
    dsn=_DSN,
    min=int(os.getenv("VECTOR_DB_POOL_MIN", "2")),
    max=int(os.getenv("VECTOR_DB_POOL_SIZE", "5")),
    increment=1,
)
# ─────────────────────────────────────────────────────────────────────────────


def _to_vec(values: List[float]) -> array.array:
    return array.array("f", values)


def _search_sync(vec: array.array, top_k: int) -> List[Dict[str, Any]]:
    sql = """
        SELECT doc_id,
               payload,
               VECTOR_DISTANCE(embedding, :query_vec, COSINE) AS distance
        FROM   mldsdev.document_vectors
        ORDER  BY VECTOR_DISTANCE(embedding, :query_vec, COSINE)
        FETCH  FIRST :top_k ROWS ONLY
    """
    results = []
    with _pool.acquire() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, query_vec=vec, top_k=top_k)
            for doc_id, payload_raw, distance in cur.fetchall():
                payload = json.loads(payload_raw) if isinstance(payload_raw, str) else payload_raw
                results.append({"doc_id": doc_id, "score": 1.0 - distance, "payload": payload})
    return results


def _execute_json_procedure_sync(procedure_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Convert input payload dictionary directly to raw JSON string for the CLOB input
    json_payload_str = json.dumps(payload)

    with _pool.acquire() as conn:
        with conn.cursor() as cur:
            # Bind an empty CLOB target variable to safely capture the OUT response
            out_response = cur.var(oracledb.DB_TYPE_CLOB)

            # Dynamically execute whichever procedure string is passed in
            cur.callproc(procedure_name, [json_payload_str, out_response])

            # Read out the text data from the returned CLOB locator safely
            response_lob = out_response.getvalue()
            response_str = response_lob.read() if response_lob else "{}"
            return json.loads(response_str)


def _execute_named_procedure_sync(
    procedure_name: str,
    payload: Dict[str, Any],
    param_keys: List[str],
) -> Dict[str, Any]:
    """
    Calls a procedure whose parameters are individual typed IN values (no OUT CLOB).
    Extracts values from the payload dict in the order declared by param_keys,
    matching the positional argument order of the Oracle procedure.
    """
    with _pool.acquire() as conn:
        with conn.cursor() as cur:
            # build the positional argument list in the declared key order
            params = [payload.get(k) for k in param_keys]

            # execute the procedure — no OUT parameter to bind
            cur.callproc(procedure_name, params)

            # explicit commit for DML procedures that do not commit internally
            conn.commit()

    return {"status": "SUCCESS", "message": "Procedure executed successfully."}


class VectorDBConnector:
    """Handles vector search and dynamic JSON package/procedure execution against Oracle 23ai."""

    async def search(self, query_vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        vec = _to_vec(query_vector)
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(None, _search_sync, vec, top_k)
        logger.info("vector_search_done", top_k=top_k, returned=len(results))
        return results

    async def execute_procedure(self, procedure_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a procedure that accepts an IN CLOB (JSON) and returns an OUT CLOB (JSON).
        call_type: json_clob
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            _execute_json_procedure_sync,
            procedure_name,
            payload,
        )
        logger.info("procedure_executed", target=procedure_name)
        return results

    async def execute_named_procedure(
        self,
        procedure_name: str,
        payload: Dict[str, Any],
        param_keys: List[str],
    ) -> Dict[str, Any]:
        """
        Executes a procedure with individual typed IN parameters and no OUT CLOB.
        call_type: named_params
        param_keys must match the positional argument order of the Oracle procedure.
        """
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            _execute_named_procedure_sync,
            procedure_name,
            payload,
            param_keys,
        )
        logger.info("named_procedure_executed", target=procedure_name)
        return results