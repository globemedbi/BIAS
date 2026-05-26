"""
Communicator request router — sends claim requests to the Orchestrator.
"""
import os
from typing import Any, Dict

import httpx

from shared.communication_layer.logger import get_logger
from shared.communication_layer.retry_handler import with_retry

logger = get_logger("COMMUNICATOR")

ORCHESTRATOR_URL = f"http://{os.getenv('ORCHESTRATOR_HOST', 'orchestrator')}:{os.getenv('ORCHESTRATOR_PORT', '8001')}"
TIMEOUT_SECONDS = 10.0


async def request_flight_plan(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sends a plan creation request to the Orchestrator."""

    async def _call() -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(f"{ORCHESTRATOR_URL}/plan/create", json=payload)
            response.raise_for_status()
            return response.json()

    return await with_retry(
        _call,
        max_attempts=3,
        service_name="COMMUNICATOR",
        operation_name="request_flight_plan",
    )
