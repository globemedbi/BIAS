"""
Logging DB connector — PostgreSQL audit event store and service registry persistence.
Every service in BIAS writes audit events here via db-agent.
"""

# asyncpg is a native async PostgreSQL driver
import asyncpg

# os reads the logging database URL from the environment
import os

# json serializes dicts into PostgreSQL JSONB columns
import json

# type hints for all function signatures
from typing import Any, Dict, Optional

# shared structured logger — every log line is tagged "DB_AGENT"
from shared.communication_layer.logger import get_logger

# creates the module logger instance
logger = get_logger("DB_AGENT")

# reads the logging PostgreSQL DSN from the environment
# expected format: postgresql://user:password@host:5432/logging_db
LOGGING_DB_URL = os.getenv("LOGGING_DB_URL", "")

# module-level pool — created once on first use, then reused for the process lifetime
_pool: Optional[asyncpg.Pool] = None


async def _get_pool() -> asyncpg.Pool:
    """Creates the logging DB pool on first call, then returns the cached pool."""

    # reference the module-level variable so we can assign to it
    global _pool

    # only create the pool once — subsequent calls reuse it
    if _pool is None:

        # open the PostgreSQL connection pool
        _pool = await asyncpg.create_pool(
            # the connection string read from .env
            dsn=LOGGING_DB_URL,
            # keep 2 connections open — audit writes happen frequently from all services
            min_size=2,
            # allow up to 10 simultaneous writers before requests queue
            max_size=10,
        )

        # log pool creation so operators can verify logging DB connectivity
        logger.info("logging_db_pool_created")

    # return the existing or newly created pool
    return _pool


class LoggingDBConnector:
    """Writes audit events and persists the Orchestrator service registry."""

    async def write_audit_event(self, event: Dict[str, Any]) -> bool:
        """Inserts one audit event row into the audit_events table."""

        # get the shared pool
        pool = await _get_pool()

        # extract each field from the event dict with a safe default of None
        # these match the columns of the audit_events table
        sql = (
            "INSERT INTO audit_events "
            "(plan_id, stage, service, event_type, message, error_code, created_at) "
            "VALUES ($1, $2, $3, $4, $5, $6, NOW())"
        )

        # borrow a connection for the INSERT
        async with pool.acquire() as conn:

            # execute the INSERT — positional args bind to $1..$6 in order
            await conn.execute(
                sql,
                # $1: the Flight Plan ID that this event belongs to
                event.get("plan_id"),
                # $2: the stage number within the Flight Plan where the event occurred
                event.get("stage"),
                # $3: the name of the service that emitted this event
                event.get("service"),
                # $4: a category label like "CLAIM_PROCESSED" or "ERROR"
                event.get("event_type"),
                # $5: human-readable description of what happened
                event.get("message"),
                # $6: optional error code — None if this is a success event
                event.get("error_code"),
            )

        # log that the audit event was written — this log goes to structlog, not the DB
        logger.info("audit_event_written", plan_id=event.get("plan_id"))

        # True signals success to the caller
        return True

    async def write_registry(self, registry_data: Dict[str, Any]) -> bool:
        """Persists the Orchestrator service registry snapshot as a JSONB row."""

        # get the shared pool
        pool = await _get_pool()

        # serialize the registry dictionary to a JSON string for the JSONB column
        registry_json = json.dumps(registry_data)

        # INSERT a new snapshot row — we keep history, never overwrite
        # each call to write_registry adds one new row with a timestamp
        sql = (
            "INSERT INTO service_registry (registry_data, saved_at) "
            "VALUES ($1::jsonb, NOW())"
        )

        # borrow a connection for the write
        async with pool.acquire() as conn:

            # execute the INSERT — $1 is the JSON string cast to jsonb by PostgreSQL
            await conn.execute(sql, registry_json)

        # log that the registry was persisted
        logger.info("registry_written", service_count=len(registry_data))

        # True signals success
        return True

    async def load_registry(self) -> Dict[str, Any]:
        """Loads the most recently saved service registry snapshot."""

        # get the shared pool
        pool = await _get_pool()

        # ORDER BY saved_at DESC LIMIT 1 returns only the latest snapshot row
        sql = (
            "SELECT registry_data "
            "FROM service_registry "
            "ORDER BY saved_at DESC "
            "LIMIT 1"
        )

        # borrow a connection for the read
        async with pool.acquire() as conn:

            # fetchrow returns None if the table is empty (first startup before any save)
            row = await conn.fetchrow(sql)

        # if no registry has ever been saved, return an empty dict
        # the Orchestrator will rebuild its registry from scratch
        if row is None:
            logger.info("registry_not_found_returning_empty")
            return {}

        # row["registry_data"] is already a Python dict because asyncpg auto-parses JSONB
        registry = row["registry_data"]

        # log how many services were loaded from the saved snapshot
        logger.info("registry_loaded", service_count=len(registry))

        # return the registry dict to the caller
        return registry
