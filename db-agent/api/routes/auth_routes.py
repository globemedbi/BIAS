"""
DB Agent authorization routes.
"""
from fastapi import APIRouter, HTTPException, Header
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("DB_AGENT")
router = APIRouter()


@router.post("/fetch")
async def fetch_authorization(
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Fetches authorization and coverage records for a claim."""
    logger.info("authorization_fetch_requested", from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")
