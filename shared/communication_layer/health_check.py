"""
BIAS Health Check Utilities
Shared health probe logic for service-to-service health checks.
"""
from typing import Dict, Optional

import httpx
import structlog

logger = structlog.get_logger()

HEALTH_TIMEOUT_SECONDS = 5.0


async def probe_service(service_name: str, url: str) -> Dict[str, object]:
    """
    Probes a single service health endpoint.

    Args:
        service_name: Human-readable service name for logging
        url: Full URL of the health endpoint

    Returns:
        Dict with keys: service, healthy, status_code, error
    """
    try:
        async with httpx.AsyncClient(timeout=HEALTH_TIMEOUT_SECONDS) as client:
            response = await client.get(url)
            healthy = response.status_code == 200
            logger.info(
                "health_probe",
                service=service_name,
                url=url,
                healthy=healthy,
                status_code=response.status_code,
            )
            return {
                "service": service_name,
                "healthy": healthy,
                "status_code": response.status_code,
                "error": None,
            }
    except Exception as e:
        logger.warning(
            "health_probe_failed",
            service=service_name,
            url=url,
            error=str(e),
        )
        return {
            "service": service_name,
            "healthy": False,
            "status_code": None,
            "error": str(e),
        }


async def probe_all_services(registry: Dict[str, str]) -> Dict[str, Dict[str, object]]:
    """
    Probes all services in the registry concurrently.

    Args:
        registry: Dict mapping service name to base URL

    Returns:
        Dict mapping service name to probe result
    """
    import asyncio

    tasks = {
        name: probe_service(name, f"{url}/health")
        for name, url in registry.items()
    }
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    return dict(zip(tasks.keys(), results))
