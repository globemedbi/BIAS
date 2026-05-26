"""
Claims Expert audit routes.
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan
from shared.models.response import AcceptedResponse, SuccessResponse

logger = get_logger("CLAIMS_EXPERT")
router = APIRouter()

_audits: dict = {}


class AuditRequest(BaseModel):
    flight_plan: FlightPlan


@router.post("/audit", response_model=AcceptedResponse, status_code=202)
async def start_audit(request: AuditRequest) -> AcceptedResponse:
    """Starts a full claim audit. Returns 202 immediately."""
    audit_id = str(uuid.uuid4())
    _audits[audit_id] = {"status": "IN_PROGRESS"}
    logger.info(
        "audit_started",
        audit_id=audit_id,
        plan_id=request.flight_plan.flight_plan_metadata.plan_id,
    )
    return AcceptedResponse(
        service="CLAIMS_EXPERT",
        job_id=audit_id,
        poll_url=f"/api/v1/audit/status/{audit_id}",
    )


@router.get("/audit/status/{audit_id}")
async def get_audit_status(audit_id: str) -> SuccessResponse:
    """Returns the status of an ongoing audit."""
    audit = _audits.get(audit_id)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return SuccessResponse(service="CLAIMS_EXPERT", data=audit)


@router.get("/summary/{claim_id}")
async def get_summary(claim_id: str) -> SuccessResponse:
    """Returns the Master Summary for a completed claim audit."""
    logger.info("summary_requested", claim_id=claim_id)
    raise HTTPException(status_code=501, detail="Not implemented")
