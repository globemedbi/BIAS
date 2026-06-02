"""
DB Agent — Security Layer (Layer 2).

Every inbound request passes through this module before any database is touched.
Two checks run in sequence:
    1. Token validation  — rejects callers that don't supply INTERNAL_SERVICE_TOKEN
    2. Registry check    — rejects routes absent from routing_registry.yaml
Only requests that pass both checks are forwarded to the router (Layer 3).
"""
import os
from typing import Any, Dict

# Layer 3: the route dispatcher — only called after both security checks pass
from agent.router import dispatch

# routing_registry: loaded from routing_registry.yaml at startup
# is_registered()           — True if the route appears in the YAML whitelist
# get_required_input_keys() — returns the declared input_keys list for the route
from agent.routing_registry import is_registered, get_required_input_keys

from shared.communication_layer.logger import get_logger

# all log lines from this module are tagged DB_AGENT
logger = get_logger("DB_AGENT")


class DBAgent:
    """
    Entry point for all inbound db-agent requests.

    Check order:
        1. validate_service_token()   — INTERNAL_SERVICE_TOKEN header check
        2. registry check             — route must exist in routing_registry.yaml
        3. payload key validation     — warns if declared input keys are missing
        4. dispatch()                 — forwards to the correct DB connector
    """

    def validate_service_token(self, token: str, service_name: str) -> bool:
        """
        Compares the caller's token against INTERNAL_SERVICE_TOKEN env var.
        Returns False (and logs a warning) if the token is missing or wrong.
        """
        # read the expected token from the environment — must be set in .env
        expected = os.getenv("INTERNAL_SERVICE_TOKEN", "")

        # reject if the env var is not configured or the tokens don't match
        if not expected or token != expected:
            logger.warning("invalid_service_token", service=service_name)
            return False

        return True

    async def handle(
        self,
        route: str,
        payload: Dict[str, Any],
        token: str,
        service_name: str,
    ) -> Dict[str, Any]:
        """
        Runs all security checks, then dispatches to the route handler.

        Raises:
            PermissionError — bad or missing service token  (HTTP 401)
            KeyError        — route not in routing registry (HTTP 400/422)
        """

        # ── CHECK 1: TOKEN VALIDATION ─────────────────────────────────────────
        # any caller without the correct internal token is rejected immediately
        # before the route name or payload are even examined
        if not self.validate_service_token(token, service_name):
            raise PermissionError(
                f"Service '{service_name}' supplied an invalid or missing token"
            )

        # ── CHECK 2: ROUTING REGISTRY WHITELIST ───────────────────────────────
        # the route must exist as an entry in routing_registry.yaml
        # routes not in the YAML were never formally documented → blocked
        if not is_registered(route):
            logger.warning(
                "route_blocked_not_in_registry",
                route=route,
                service=service_name,
            )
            raise KeyError(
                f"Route '{route}' is not registered in routing_registry.yaml. "
                "Add a block for it under 'routes:' and restart the service."
            )

        # ── CHECK 3: PAYLOAD KEY VALIDATION (soft) ────────────────────────────
        # compare the incoming payload keys against the 'Parsed Input Keys'
        # column in the Excel — warn on missing keys but do NOT block the request
        # (the database procedure itself will produce a clear error if a key is absent)
        required_keys = get_required_input_keys(route)
        if required_keys:
            missing = [k for k in required_keys if k not in payload]
            if missing:
                logger.warning(
                    "payload_missing_declared_keys",
                    route=route,
                    service=service_name,
                    missing_keys=missing,
                )

        # ── DISPATCH ──────────────────────────────────────────────────────────
        # all checks passed — forward to Layer 3 (agent/router.py)
        logger.info("request_accepted", route=route, service=service_name)
        return await dispatch(route, payload)


# singleton — all route modules import this one instance
db_agent = DBAgent()
