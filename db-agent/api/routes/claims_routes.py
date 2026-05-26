"""
DB Agent claims data routes.
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("DB_AGENT")
router = APIRouter()


@router.post("/store")
async def store_claim(
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Stores OCR extraction results for a claim."""
    logger.info("claim_store_requested", from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/history")
async def get_claim_history(
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Returns member claim history."""
    logger.info("claim_history_requested", from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")
