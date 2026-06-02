"""
DB Agent — Security Layer (Layer 2).

Validates caller identity via X-Service-Token before any payload reaches the router.
This module is the single import point for the generic /execute-procedure endpoint.
All existing route files continue to import from agent.db_agent — both resolve to
the same singleton instance so token validation behaviour is identical everywhere.
"""

# import the fully-initialised singleton from its canonical home
# re-exporting it here lets api/routes.py use "from agent.agent import db_agent"
# without duplicating the class definition
from agent.db_agent import db_agent  # noqa: F401  — re-exported intentionally
