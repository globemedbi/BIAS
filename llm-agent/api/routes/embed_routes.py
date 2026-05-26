"""
LLM Agent embedding routes.
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("LLM_AGENT")
router = APIRouter()


class EmbedRequest(BaseModel):
    text: str
    model: Optional[str] = None


@router.post("/embed")
async def embed(
    request: EmbedRequest,
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Generates vector embeddings for the provided text."""
    logger.info("embed_requested", from_service=x_service_name)
    raise HTTPException(status_code=501, detail="Not implemented")
