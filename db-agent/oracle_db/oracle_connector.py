"""
Oracle 23ai connector — schema: mldsdev.
Single shared connection pool for all Oracle operations in db-agent.
Stored-procedure calls are the primary interface; raw SQL is a secondary fallback.
"""
import asyncio
import json
import os
from typing import Any, Dict

import oracledb

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

# ── Pool — opened once at import time ────────────────────────────────────────
oracledb.init_oracle_client()   # thick mode — Oracle Instant Client required

_DSN = (
    "(DESCRIPTION="
    "(ADDRESS=(PROTOCOL=TCP)(HOST=192.168.244.198)(PORT=1528))"
    "(CONNECT_DATA=(SERVICE_NAME=aidev_pdb1.drdb.drdatabase.oraclevcn.com)))"
)

pool = oracledb.create_pool(
    user=os.getenv("VECTOR_DB_USER", "mldsdev"),
    password=os.getenv("VECTOR_DB_PASSWORD", "MLDSDEVai25"),
    dsn=_DSN,
    min=int(os.getenv("VECTOR_DB_POOL_MIN", "2")),
    max=int(os.getenv("VECTOR_DB_POOL_SIZE", "5")),
    increment=1,
)

logger.info("oracle_pool_created", host="192.168.244.198", port=1528)
# ─────────────────────────────────────────────────────────────────────────────


def _call_proc_sync(proc_name: str, json_payload: str) -> Dict[str, Any]:
    """
    Calls an Oracle stored procedure with signature:
        proc(p_json_payload IN CLOB, p_json_response OUT CLOB)
    Returns the OUT parameter parsed as a Python dict.
    """
    with pool.acquire() as conn:
        with conn.cursor() as cur:
            out_var = cur.var(oracledb.DB_TYPE_CLOB)
            cur.callproc(proc_name, [json_payload, out_var])
            conn.commit()

            raw = out_var.getvalue()
            if raw is None:
                return {}

            # CLOB value: call .read() if it's a LOB object, else use directly
            text = raw.read() if hasattr(raw, "read") else str(raw)
            return json.loads(text)


async def call_procedure(proc_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Async wrapper — runs the blocking Oracle call in a thread pool so the
    FastAPI event loop is never blocked.
    """
    json_in = json.dumps(payload)
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _call_proc_sync, proc_name, json_in)
    logger.info("procedure_called", proc=proc_name)
    return result
