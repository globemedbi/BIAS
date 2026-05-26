"""
Logging DB connector — write-only store for audit events.
"""
import os
from typing import Any, Dict

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

LOGGING_DB_URL = os.getenv("LOGGING_DB_URL", "")


class LoggingDBConnector:
    """Write-only connector for the audit logging database."""

    async def write_audit_event(self, event: Dict[str, Any]) -> bool:
        """Writes an audit event record."""
        raise NotImplementedError

    async def write_registry(self, registry_data: Dict[str, Any]) -> bool:
        """Persists the service registry."""
        raise NotImplementedError

    async def load_registry(self) -> Dict[str, Any]:
        """Loads the persisted service registry."""
        raise NotImplementedError
