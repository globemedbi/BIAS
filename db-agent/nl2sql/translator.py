"""
NL2SQL Translator — converts natural language questions to safe SQL SELECT queries.
Translation is performed by the LLM Agent (port 8005) — db-agent never calls an LLM directly.
"""

# os reads the LLM Agent URL from the environment so it never has to be hardcoded
import os

# httpx is the HTTP client used for all internal service calls in BIAS
import httpx

# type hints for function signatures
from typing import Optional

# shared structured logger
from shared.communication_layer.logger import get_logger

# creates the module logger instance tagged "DB_AGENT"
logger = get_logger("DB_AGENT")

# the URL of the LLM Agent service — reads from env, falls back to the Docker service name
LLM_AGENT_URL = os.getenv("LLM_AGENT_URL", "http://llm-agent:8005")

# the internal service token required by every BIAS internal endpoint
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")

# tables that NL2SQL is allowed to query — any table not in this set is forbidden
# frozenset is immutable so no code path can accidentally expand the whitelist at runtime
ALLOWED_TABLES = frozenset([
    "claims",
    "members",
    "authorizations",
    "claim_history",
    "coverage_plans",
])

# SQL keywords that must never appear in a generated query
# covers all data-modifying and schema-altering operations
BLOCKED_KEYWORDS = frozenset([
    "delete", "update", "insert", "drop", "alter", "truncate",
    "create", "grant", "revoke", "exec", "execute",
])

# the system context sent to the LLM so it knows which tables and columns exist
# this prevents hallucinated table names that don't exist in the schema
_SCHEMA_CONTEXT = """
You are a SQL generator for the BIAS insurance claims PostgreSQL database.
Generate only safe, read-only SELECT queries.

Available tables and key columns:
- claims(claim_id, member_id, claim_type, status, amount, created_at)
- members(member_id, name, plan_id, date_of_birth)
- authorizations(claim_id, authorized, authorization_code, authorized_amount, decision_date, plan_id)
- claim_history(claim_id, member_id, claim_type, status, amount, created_at)
- coverage_plans(plan_id, plan_name, coverage_type, deductible, copay)

Rules:
- Output ONLY the raw SQL — no markdown, no explanation, no code fences.
- Use only the tables listed above.
- Use only SELECT statements.
- Always use parameterized references — never inline user values.
- If the question cannot be answered with these tables, output: CANNOT_TRANSLATE
"""


def is_safe_query(sql: str) -> bool:
    """Returns True only if the SQL contains none of the blocked keywords."""

    # lowercase the entire string so "DELETE", "Delete", and "delete" are all caught
    lower_sql = sql.lower()

    # any() short-circuits on first match — returns True if ANY keyword is found
    # the not inverts it: we return True only when NO blocked keyword is present
    return not any(kw in lower_sql for kw in BLOCKED_KEYWORDS)


async def translate(natural_language_query: str) -> Optional[str]:
    """
    Sends the query to LLM Agent for SQL generation.
    Validates the result against the safety filter.
    Returns None if translation fails or produces unsafe SQL.
    """

    # log the incoming request — never log the raw query text as it may contain PII
    logger.info("nl2sql_translate_requested")

    # build the request body for the LLM Agent /api/v1/complete endpoint
    llm_request = {
        # "extract" is the task type for structured data extraction / generation
        "task_type": "extract",
        # BALANCED trades off speed vs. quality — appropriate for SQL generation
        "model_preference": "BALANCED",
        # the schema context tells the LLM what tables it can use
        "context": _SCHEMA_CONTEXT,
        # the user's original natural language question is the input
        "input": natural_language_query,
        # 500 tokens is plenty for a single SELECT statement
        "max_tokens": 500,
    }

    # make an HTTP POST to the LLM Agent service
    try:

        # create a short-lived HTTP client for this single call
        async with httpx.AsyncClient(base_url=LLM_AGENT_URL, timeout=30.0) as client:

            # POST to the LLM Agent completion endpoint
            response = await client.post(
                "/api/v1/complete",
                # send the request body as JSON
                json=llm_request,
                # include the internal service token and caller identity headers
                headers={
                    "X-Service-Token": INTERNAL_SERVICE_TOKEN,
                    "X-Service-Name": "DB_AGENT",
                },
            )

        # raise an exception if the LLM Agent returned a non-2xx status
        response.raise_for_status()

    # catches network errors — LLM Agent may not be running yet in early development
    except httpx.ConnectError:
        logger.error("llm_agent_unreachable", url=LLM_AGENT_URL)
        # return None — caller will surface a 503 error to the requesting agent
        return None

    # catches HTTP 4xx/5xx responses from LLM Agent
    except httpx.HTTPStatusError as exc:
        logger.error("llm_agent_error", status=exc.response.status_code)
        return None

    # parse the LLM Agent JSON response body
    llm_response = response.json()

    # navigate to the generated SQL — it lives in data.content per the API contract
    sql = llm_response.get("data", {}).get("content", "").strip()

    # if the LLM decided it cannot answer, return None rather than an empty string
    if not sql or sql == "CANNOT_TRANSLATE":
        logger.warning("nl2sql_cannot_translate")
        return None

    # run the generated SQL through the safety filter before it can ever be executed
    if not is_safe_query(sql):
        # log a warning — this should never happen if the LLM followed the schema context
        logger.warning("nl2sql_generated_unsafe_sql")
        # return None — the unsafe SQL is discarded, never executed
        return None

    # log success with the first 100 characters of the SQL for debugging
    logger.info("nl2sql_translated", sql_preview=sql[:100])

    # return the validated SQL — the caller will execute it against the target database
    return sql
