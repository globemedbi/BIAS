"""
BIAS Shared Claim Model
Unified claim data structure used across all services.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ClaimTypeEnum(str, Enum):
    MEDICAL = "MEDICAL"
    DENTAL = "DENTAL"
    VISION = "VISION"
    PHARMACY = "PHARMACY"


class ClaimStatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class PriorityEnum(str, Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class FileAttachment(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    uri: str
    size_bytes: Optional[int] = None


class Claim(BaseModel):
    """
    Core claim data model shared across all BIAS services.
    """
    claim_id: str
    member_id: str
    claim_type: ClaimTypeEnum
    priority: PriorityEnum = PriorityEnum.NORMAL
    status: ClaimStatusEnum = ClaimStatusEnum.SUBMITTED
    submitted_by: str
    file_attachments: List[FileAttachment] = []
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    plan_id: Optional[str] = None
    request_id: Optional[str] = None
