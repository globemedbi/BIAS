"""
Orchestrator health monitor — probes all services every 30 seconds.
"""
import asyncio
from typing import TYPE_CHECKING

from shared.communication_layer.health_check import probe_service
from shared.communication_layer.logger import get_logger

if TYPE_CHECKING:
    from orchestrator.service_registry.registry import ServiceRegistry

logger = get_logger("ORCHESTRATOR")

PROBE_INTERVAL_SECONDS = 30


async def run_health_monitor(registry: "ServiceRegistry") -> None:
    """Continuously probes all registered services and updates registry health."""
    while True:
        entries = registry.all_entries()
        for service_name, entry in entries.items():
            result = await probe_service(service_name, f"{entry['url']}/health")
            if result["healthy"]:
                registry.mark_healthy(service_name)
            else:
                registry.mark_unhealthy(service_name)
        await asyncio.sleep(PROBE_INTERVAL_SECONDS)
