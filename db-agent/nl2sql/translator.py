"""
NL2SQL Translator — safely converts natural language to SQL SELECT queries.
"""
from typing import List, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

ALLOWED_TABLES = frozenset([
    "claims",
    "members",
    "authorizations",
    "claim_history",
    "coverage_plans",
])

BLOCKED_KEYWORDS = frozenset([
    "delete", "update", "insert", "drop", "alter", "truncate",
    "create", "grant", "revoke", "exec", "execute",
])


def is_safe_query(sql: str) -> bool:
    """Returns True if the SQL contains no blocked keywords."""
    lower_sql = sql.lower()
    return not any(kw in lower_sql for kw in BLOCKED_KEYWORDS)


def translate(natural_language_query: str) -> Optional[str]:
    """
    Converts a natural language query to a safe SQL SELECT statement.
    Returns None if translation is not possible or unsafe.
    """
    raise NotImplementedError
