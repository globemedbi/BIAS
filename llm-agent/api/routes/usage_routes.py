"""
LLM Agent usage reporting routes.
"""
from fastapi import APIRouter, HTTPException

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("LLM_AGENT")
router = APIRouter()


@router.get("/report")
async def usage_report() -> SuccessResponse:
    """Returns token usage statistics per calling service."""
    raise HTTPException(status_code=501, detail="Not implemented")
