"""
Orchestrator service registry routes.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("ORCHESTRATOR")
router = APIRouter()


class RegisterServiceRequest(BaseModel):
    service_name: str
    url: str
    port: int


@router.post("/register")
async def register_service(request: RegisterServiceRequest) -> SuccessResponse:
    """Registers a service in the registry with its URL."""
    logger.info("service_register_requested", service=request.service_name, url=request.url)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("")
async def get_registry() -> SuccessResponse:
    """Returns all registered services and their health status."""
    logger.info("registry_requested")
    raise HTTPException(status_code=501, detail="Not implemented")
