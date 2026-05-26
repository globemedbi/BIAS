"""
Token governance — tracks and enforces per-service token budgets.
"""
from collections import defaultdict
from typing import Dict

from shared.communication_layer.logger import get_logger

logger = get_logger("LLM_AGENT")

# Per-service token counts for Phase 1 (in-memory)
_token_usage: Dict[str, int] = defaultdict(int)


def record_usage(service_name: str, tokens_used: int) -> None:
    """Records token usage for a calling service."""
    _token_usage[service_name] += tokens_used
    logger.info("token_usage_recorded", service=service_name, tokens=tokens_used, total=_token_usage[service_name])


def get_usage_report() -> Dict[str, int]:
    """Returns the current token usage per service."""
    return dict(_token_usage)


def reset_usage(service_name: str) -> None:
    """Resets token count for a service (e.g., monthly reset)."""
    _token_usage[service_name] = 0
