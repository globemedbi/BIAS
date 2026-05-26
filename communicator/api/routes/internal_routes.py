"""
Communicator internal routes — receives callbacks from other services.
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("COMMUNICATOR")
router = APIRouter()


@router.post("/callback")
async def receive_callback(
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Receives the final result callback from Chatbot."""
    logger.info("callback_received", from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/health")
async def internal_health() -> dict:
    """Internal health check."""
    return {"service": "COMMUNICATOR", "status": "HEALTHY"}
