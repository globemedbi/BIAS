"""
Legacy DB connector — on-premise PostgreSQL database.
Handles all claim, member, authorization, and OCR storage operations.
"""

# asyncpg is a native async PostgreSQL driver — no blocking I/O, no thread wrappers needed
import asyncpg

# os reads the database URL from the environment — never hardcoded here
import os

# json serializes OCR data dicts into PostgreSQL JSONB column format
import json

# type hints keep function signatures readable and enable IDE + mypy checking
from typing import Any, Dict, List, Optional

# shared structured logger — every log line is tagged "DB_AGENT"
from shared.communication_layer.logger import get_logger

# creates the module-level logger instance
logger = get_logger("DB_AGENT")

# reads the full PostgreSQL DSN from the environment
# expected format: postgresql://user:password@host:5432/legacy_db
LEGACY_DB_URL = os.getenv("LEGACY_DB_URL", "")

# module-level pool — None until the first database call, then shared forever
_pool: Optional[asyncpg.Pool] = None


async def _get_pool() -> asyncpg.Pool:
    """Creates the connection pool on first call, then returns the cached pool."""

    # tell Python we are assigning to the module-level variable, not a new local one
    global _pool

    # skip creation if the pool already exists
    if _pool is None:

        # asyncpg.create_pool dials PostgreSQL and opens min_size live connections
        _pool = await asyncpg.create_pool(
            # the connection string read from .env
            dsn=LEGACY_DB_URL,
            # always keep 2 connections open so the first request never waits for a dial
            min_size=2,
            # cap at 10 simultaneous connections; extra requests queue inside asyncpg
            max_size=10,
        )

        # log pool creation so operators can confirm connectivity at startup
        logger.info("legacy_db_pool_created")

    # return the pool — either the one just created or the one already cached
    return _pool


class LegacyDBConnector:
    """Handles all read and write operations against the legacy PostgreSQL database."""

    async def fetch_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Fetches a single claim record by claim_id. Returns None if not found."""

        # get (or lazily create) the shared connection pool
        pool = await _get_pool()

        # $1 is asyncpg's positional bind parameter — the driver never formats
        # the value into the SQL string, which eliminates SQL injection by design
        sql = "SELECT * FROM claims WHERE claim_id = $1"

        # acquire() borrows one connection from the pool for the duration of the block
        # the connection is automatically returned when the with-block exits
        async with pool.acquire() as conn:

            # fetchrow executes the query and returns exactly one Record, or None
            row = await conn.fetchrow(sql, claim_id)

        # if no matching row was found, signal absence rather than raising an exception
        if row is None:
            return None

        # asyncpg Record objects behave like dicts but must be converted explicitly
        return dict(row)

    async def fetch_member_history(self, member_id: str) -> List[Dict[str, Any]]:
        """Returns all historical claims for a member, ordered newest first."""

        # get the shared pool
        pool = await _get_pool()

        # select the columns callers need — avoids sending internal columns over the wire
        # ORDER BY created_at DESC places the most recent claim at index 0
        sql = (
            "SELECT claim_id, claim_type, status, amount, created_at "
            "FROM claim_history "
            "WHERE member_id = $1 "
            "ORDER BY created_at DESC"
        )

        # borrow a connection for this query
        async with pool.acquire() as conn:

            # fetch returns a list of Record objects — one per row; empty list if no rows
            rows = await conn.fetch(sql, member_id)

        # convert every Record to a plain dict so callers receive standard Python objects
        return [dict(row) for row in rows]

    async def fetch_authorization(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Fetches authorization status and coverage details for a claim."""

        # get the shared pool
        pool = await _get_pool()

        # LEFT JOIN coverage_plans brings coverage details into the same row
        # LEFT JOIN means we still return the authorization even if no plan row exists
        sql = (
            "SELECT a.claim_id, a.authorized, a.authorization_code, "
            "       a.authorized_amount, a.decision_date, "
            "       c.plan_name, c.coverage_type, c.deductible, c.copay "
            "FROM   authorizations a "
            "LEFT JOIN coverage_plans c ON a.plan_id = c.plan_id "
            "WHERE  a.claim_id = $1"
        )

        # borrow a connection for this query
        async with pool.acquire() as conn:

            # returns None if the claim has no authorization record yet
            row = await conn.fetchrow(sql, claim_id)

        # surface None to the caller — they decide whether to 404 or return empty data
        if row is None:
            return None

        # convert the Record to a standard dict
        return dict(row)

    async def store_ocr_result(self, claim_id: str, ocr_data: Dict[str, Any]) -> bool:
        """Stores OCR extraction data for a claim. Upserts — safe to call more than once."""

        # get the shared pool
        pool = await _get_pool()

        # convert the Python dict to a JSON string for PostgreSQL's JSONB column type
        ocr_json = json.dumps(ocr_data)

        # ON CONFLICT (claim_id): if a row already exists for this claim, update it
        # this makes the call idempotent — re-processing a document won't create duplicates
        sql = (
            "INSERT INTO ocr_results (claim_id, data, created_at) "
            "VALUES ($1, $2::jsonb, NOW()) "
            "ON CONFLICT (claim_id) "
            "DO UPDATE SET data = EXCLUDED.data, updated_at = NOW()"
        )

        # borrow a connection for the write
        async with pool.acquire() as conn:

            # execute runs an INSERT/UPDATE and does not return rows
            await conn.execute(sql, claim_id, ocr_json)

        # log the write so there is a structured audit trail for every OCR store
        logger.info("ocr_result_stored", claim_id=claim_id)

        # True signals success; the caller raises HTTP 500 if we raise instead
        return True

    async def execute_query_raw(self, sql: str) -> List[Dict[str, Any]]:
        """Executes a pre-validated SELECT query. Only called after NL2SQL safety check."""

        # get the shared pool
        pool = await _get_pool()

        # log execution — never log the SQL itself as it may reference sensitive values
        logger.info("legacy_raw_query_executing")

        # borrow a connection from the pool
        async with pool.acquire() as conn:

            # run the pre-validated SQL — no bind params needed for NL2SQL output
            rows = await conn.fetch(sql)

        # convert all Records to plain dicts and return the list
        return [dict(row) for row in rows]
