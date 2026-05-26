"""
BIAS Shared Response Models
All services MUST use these models for API responses.
No custom response shapes permitted.
"""
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class ErrorDetail(BaseModel):
    error_code: str
    message: str
    field: Optional[str] = None


class BaseResponse(BaseModel):
    """
    Mandatory base for ALL BIAS API responses.
    Every endpoint response must inherit from this.
    """
    status: StatusEnum
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class SuccessResponse(BaseResponse):
    status: StatusEnum = StatusEnum.SUCCESS
    data: Optional[Any] = None


class ErrorResponse(BaseResponse):
    status: StatusEnum = StatusEnum.FAILED
    errors: List[ErrorDetail]
    support_ref: Optional[str] = None


class AcceptedResponse(BaseResponse):
    status: StatusEnum = StatusEnum.ACCEPTED
    job_id: str
    poll_url: str


class HealthResponse(BaseModel):
    service: str
    status: str = "HEALTHY"
    version: str
    uptime_s: Optional[int] = None
    checks: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
