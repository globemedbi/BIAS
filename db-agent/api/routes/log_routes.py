"""
DB Agent audit log routes.
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("DB_AGENT")
router = APIRouter()


class AuditLogRequest(BaseModel):
    plan_id: str
    stage: int
    service: str
    event_type: str
    message: str
    error_code: Optional[str] = None


@router.post("/audit")
async def write_audit_log(
    request: AuditLogRequest,
    x_service_token: Optional[str] = Header(None),
    x_service_name: Optional[str] = Header(None),
) -> SuccessResponse:
    """Writes an audit log entry to the Logging DB."""
    logger.info("audit_log_write_requested", from_service=x_service_name, plan_id=request.plan_id)
    raise HTTPException(status_code=501, detail="Not implemented")
