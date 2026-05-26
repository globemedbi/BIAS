"""
File Management processing routes.
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan
from shared.models.response import AcceptedResponse, SuccessResponse

logger = get_logger("FILE_MANAGEMENT")
router = APIRouter()

# In-memory job store for Phase 1
_jobs: dict = {}


class ProcessRequest(BaseModel):
    flight_plan: FlightPlan
    file_uris: List[str]
    translate: bool = False
    target_language: str = "en"


@router.post("/process", response_model=AcceptedResponse, status_code=202)
async def process_files(request: ProcessRequest) -> AcceptedResponse:
    """Submits files for the OCR → Anonymize → Translate pipeline."""
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {"status": "IN_PROGRESS", "output_uris": []}
    logger.info("process_job_created", job_id=job_id, file_count=len(request.file_uris))
    return AcceptedResponse(
        service="FILE_MANAGEMENT",
        job_id=job_id,
        poll_url=f"/api/v1/process/status/{job_id}",
    )


@router.get("/process/status/{job_id}")
async def get_job_status(job_id: str) -> SuccessResponse:
    """Returns the processing status and output URIs for a job."""
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return SuccessResponse(service="FILE_MANAGEMENT", data=job)


@router.get("/extract/{claim_id}")
async def get_extracted_text(claim_id: str) -> SuccessResponse:
    """Returns the extracted text artifacts for a claim."""
    logger.info("extract_requested", claim_id=claim_id)
    raise HTTPException(status_code=501, detail="Not implemented")
