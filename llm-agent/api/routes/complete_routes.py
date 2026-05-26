"""
LLM Agent completion routes.
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("LLM_AGENT")
router = APIRouter()


class CompletionRequest(BaseModel):
    task_type: str
    model_preference: str = "BALANCED"
    context: str = ""
    input: str
    max_tokens: int = 1000


@router.post("/complete")
async def complete(
    request: CompletionRequest,
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Sends a completion request to the configured LLM provider."""
    logger.info("completion_requested", task_type=request.task_type, from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/models")
async def list_models() -> SuccessResponse:
    """Returns available models and their current status."""
    raise HTTPException(status_code=501, detail="Not implemented")
