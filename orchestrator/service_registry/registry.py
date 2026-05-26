"""
Orchestrator service registry — tracks live service URLs and health status.
"""
from datetime import datetime
from typing import Dict, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("ORCHESTRATOR")


class ServiceEntry:
    """Represents a registered service with its URL and health state."""

    def __init__(self, service_name: str, url: str, port: int) -> None:
        self.service_name = service_name
        self.url = url
        self.port = port
        self.healthy = True
        self.last_checked: Optional[datetime] = None


class ServiceRegistry:
    """In-memory service registry for Phase 1."""

    def __init__(self) -> None:
        self._entries: Dict[str, ServiceEntry] = {}

    def register(self, service_name: str, url: str, port: int) -> None:
        """Registers or updates a service entry."""
        self._entries[service_name] = ServiceEntry(service_name, url, port)
        logger.info("service_registered", service=service_name, url=url)

    def get_url(self, service_name: str) -> Optional[str]:
        """Returns the URL for a service, or None if not registered."""
        entry = self._entries.get(service_name)
        return entry.url if entry else None

    def mark_unhealthy(self, service_name: str) -> None:
        """Marks a service as unhealthy after a failed health probe."""
        if service_name in self._entries:
            self._entries[service_name].healthy = False
            logger.warning("service_marked_unhealthy", service=service_name)

    def mark_healthy(self, service_name: str) -> None:
        """Marks a service as healthy after a successful health probe."""
        if service_name in self._entries:
            self._entries[service_name].healthy = True

    def all_entries(self) -> Dict[str, dict]:
        """Returns all registry entries as dicts."""
        return {
            name: {
                "url": entry.url,
                "port": entry.port,
                "healthy": entry.healthy,
                "last_checked": entry.last_checked.isoformat() if entry.last_checked else None,
            }
            for name, entry in self._entries.items()
        }
