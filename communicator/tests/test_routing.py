"""
Tests for the Communicator request router.
"""
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_request_flight_plan_calls_orchestrator():
    """Should call the Orchestrator plan/create endpoint."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"status": "ACCEPTED", "job_id": "plan-123"}
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )
        from communicator.routing.request_router import request_flight_plan
        result = await request_flight_plan({"claim_id": "CLM-001"})
        assert result["job_id"] == "plan-123"
