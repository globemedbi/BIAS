"""
BIAS Shared Event Model
Used for audit logging and inter-service event tracking.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class EventTypeEnum(str, Enum):
    STAGE_STARTED = "STAGE_STARTED"
    STAGE_COMPLETED = "STAGE_COMPLETED"
    STAGE_FAILED = "STAGE_FAILED"
    HAND_OFF = "HAND_OFF"
    RECOVERY_TRIGGERED = "RECOVERY_TRIGGERED"
    AUDIT_WRITTEN = "AUDIT_WRITTEN"


class Event(BaseModel):
    """
    Audit event emitted by each service stage transition.
    Written to Logging DB via DB Agent.
    """
    event_id: str
    event_type: EventTypeEnum
    service: str
    plan_id: str
    stage: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
