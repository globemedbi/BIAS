"""
Orchestrator metrics routes.
"""
from fastapi import APIRouter, HTTPException

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("ORCHESTRATOR")
router = APIRouter()


@router.get("")
async def get_metrics() -> SuccessResponse:
    """Returns system-level metrics for the BI dashboard."""
    logger.info("metrics_requested")
    raise HTTPException(status_code=501, detail="Not implemented")
