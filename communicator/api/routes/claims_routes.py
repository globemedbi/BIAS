"""
Communicator external claims routes.
"""
from fastapi import APIRouter, HTTPException

from shared.communication_layer.logger import get_logger
from shared.models.response import AcceptedResponse, SuccessResponse

logger = get_logger("COMMUNICATOR")
router = APIRouter()


@router.post("/submit", response_model=AcceptedResponse, status_code=202)
async def submit_claim() -> AcceptedResponse:
    """Accepts a new claim submission. Validates JWT, uploads files, triggers Orchestrator."""
    logger.info("claim_submit_requested")
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{request_id}/status")
async def get_claim_status(request_id: str) -> SuccessResponse:
    """Returns the current processing status of a submitted claim."""
    logger.info("claim_status_requested", request_id=request_id)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/history")
async def get_claim_history() -> SuccessResponse:
    """Returns claim history for the authenticated user."""
    logger.info("claim_history_requested")
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{request_id}/report")
async def get_claim_report(request_id: str) -> SuccessResponse:
    """Returns the final Master Summary report for a completed claim."""
    logger.info("claim_report_requested", request_id=request_id)
    raise HTTPException(status_code=501, detail="Not implemented")
