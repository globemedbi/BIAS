"""
DB Agent — Routing Registry Loader (Layer 2 guard).

Reads routing_registry.yaml once at startup and builds an in-memory lookup table.
Every inbound route is checked against this table before the payload is forwarded
to any database. Routes absent from the YAML are rejected at the agent layer —
they never reach the router or any database connector.

The YAML lives at: db-agent/routing_registry.yaml
Edit that file directly to add or remove routes, then restart the service.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

# ── FILE LOCATION ─────────────────────────────────────────────────────────────

# __file__ = db-agent/agent/routing_registry.py
# .parent   = db-agent/agent/
# .parent.parent = db-agent/   ← where routing_registry.yaml lives
_REGISTRY_YAML = Path(__file__).parent.parent / "routing_registry.yaml"


# ── YAML LOADER ───────────────────────────────────────────────────────────────

def _load_from_yaml(path: Path) -> Dict[str, Any]:
    """
    Parses routing_registry.yaml and returns the routes dict keyed by route name.
    Logs a warning and returns an empty dict if the file is missing or malformed.
    """

    # guard: warn and degrade gracefully if the file was never created
    if not path.exists():
        logger.warning(
            "routing_registry_yaml_missing",
            path=str(path),
            hint="Create routing_registry.yaml in db-agent/",
        )
        return {}

    with open(path, "r", encoding="utf-8") as f:
        # safe_load prevents arbitrary Python object deserialisation
        doc = yaml.safe_load(f)

    # the YAML must have a top-level 'routes' key
    routes = doc.get("routes") if isinstance(doc, dict) else None

    if not isinstance(routes, dict):
        logger.error(
            "routing_registry_yaml_invalid",
            path=str(path),
            hint="Top-level 'routes:' key is missing or not a mapping",
        )
        return {}

    logger.info("routing_registry_loaded", route_count=len(routes), source="yaml")
    return routes


# ── SINGLETON — loaded once at import time ────────────────────────────────────

_REGISTRY: Dict[str, Any] = _load_from_yaml(_REGISTRY_YAML)


# ── PUBLIC API ────────────────────────────────────────────────────────────────

def is_registered(route: str) -> bool:
    """
    Returns True if the route exists in routing_registry.yaml.
    Called by db_agent.handle() before every dispatch — absent routes are blocked.
    """
    return route in _REGISTRY


def lookup(route: str) -> Optional[Dict]:
    """
    Returns the full YAML block for a route, or None if the route is absent.
    Contains: api_endpoint, http_method, target_db, db_type, package, procedure,
              input_keys, output_keys, description, example_payload, example_response.
    """
    return _REGISTRY.get(route)


def get_required_input_keys(route: str) -> List[str]:
    """
    Returns the list of required payload keys declared under 'input_keys:' in the YAML.
    Used by db_agent.handle() to warn on missing fields before dispatch.
    Returns an empty list for routes with no required keys (e.g. load_registry).
    """
    entry = _REGISTRY.get(route)
    if not entry:
        return []

    keys = entry.get("input_keys") or []

    # input_keys is already a proper YAML list — no parsing needed
    return [str(k) for k in keys if k]


def registered_routes() -> List[str]:
    """Returns a sorted list of all route names currently in the registry."""
    return sorted(_REGISTRY.keys())
