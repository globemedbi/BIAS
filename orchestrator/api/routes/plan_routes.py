"""
Orchestrator plan management routes.
"""
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan, OverallStatusEnum, StageStatusEnum
from shared.models.response import AcceptedResponse, ErrorResponse, SuccessResponse

logger = get_logger("ORCHESTRATOR")
router = APIRouter()


class CreatePlanRequest(BaseModel):
    claim_id: str
    member_id: str
    request_type: str
    file_uris: list = []
    priority: str = "NORMAL"


class StageUpdateRequest(BaseModel):
    stage: int
    status: str
    output_uri: str = ""


@router.post("/create", response_model=AcceptedResponse, status_code=202)
async def create_plan(request: CreatePlanRequest) -> AcceptedResponse:
    """Creates a new Flight Plan for an incoming claim request."""
    logger.info("plan_create_requested", claim_id=request.claim_id, request_type=request.request_type)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{plan_id}/stage/update")
async def update_stage(plan_id: str, request: StageUpdateRequest) -> SuccessResponse:
    """Updates a stage within an existing Flight Plan."""
    logger.info("stage_update_requested", plan_id=plan_id, stage=request.stage, status=request.status)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{plan_id}/status")
async def get_plan_status(plan_id: str) -> SuccessResponse:
    """Returns the current execution state of a Flight Plan."""
    logger.info("plan_status_requested", plan_id=plan_id)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/{plan_id}/recover")
async def recover_plan(plan_id: str) -> SuccessResponse:
    """Triggers Stage 99 recovery for a failed Flight Plan."""
    logger.info("plan_recovery_requested", plan_id=plan_id)
    raise HTTPException(status_code=501, detail="Not implemented")
