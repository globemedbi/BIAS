"""
DB Agent NL2SQL query routes.
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("DB_AGENT")
router = APIRouter()


class NLQueryRequest(BaseModel):
    query: str
    target_db: str = "LEGACY"


@router.post("/nl")
async def natural_language_query(
    request: NLQueryRequest,
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Translates a natural language query to SQL and executes it safely."""
    logger.info("nl_query_requested", from_service=x_service_name, target_db=request.target_db)
    raise HTTPException(status_code=501, detail="Not implemented")
