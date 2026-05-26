"""
Chatbot format routes — formats audit results for display.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional

from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan
from shared.models.response import SuccessResponse

logger = get_logger("CHATBOT")
router = APIRouter()


class FormatRequest(BaseModel):
    flight_plan: FlightPlan
    audit_result: Dict[str, Any]
    user_type: str = "MEMBER"


@router.post("/format")
async def format_result(request: FormatRequest) -> SuccessResponse:
    """Formats a technical audit result for the specified user_type."""
    logger.info(
        "format_requested",
        user_type=request.user_type,
        plan_id=request.flight_plan.flight_plan_metadata.plan_id,
    )
    raise HTTPException(status_code=501, detail="Not implemented")
