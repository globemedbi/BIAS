"""
BIAS Flight Plan Models
Defines the structure of the Flight Plan JSON
that travels with every claim request.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RequestTypeEnum(str, Enum):
    CLAIM_AUDIT = "CLAIM_AUDIT"
    DOC_ANONYMIZATION = "DOC_ANONYMIZATION"
    CLAIM_STATUS = "CLAIM_STATUS"


class OverallStatusEnum(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED_RETRYING = "FAILED_RETRYING"
    FAILED = "FAILED"


class StageStatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ServiceRegistry(BaseModel):
    ORCHESTRATOR: str
    COMMUNICATOR: str
    FILE_MANAGEMENT: str
    DB_AGENT: str
    CLAIMS_EXPERT: str
    LLM_AGENT: str
    CHATBOT: str


class StepRouting(BaseModel):
    next_on_success: Any  # int or "COMPLETE"
    next_on_failure: int = 99
    callback_agent: Optional[str] = None


class FlightPlanStep(BaseModel):
    stage: int
    service: str
    endpoint: str
    status: StageStatusEnum = StageStatusEnum.PENDING
    routing: StepRouting
    config: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_uri: Optional[str] = None


class FlightPlanMetadata(BaseModel):
    plan_id: str
    request_id: str
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    request_type: RequestTypeEnum


class ExecutionState(BaseModel):
    overall_status: OverallStatusEnum = OverallStatusEnum.IN_PROGRESS
    current_stage: int = 0
    total_stages: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class InputData(BaseModel):
    claim_id: str
    member_id: str
    file_uris: List[str] = []


class ErrorLogEntry(BaseModel):
    stage: int
    service: str
    timestamp: datetime
    error_code: str
    message: str


class ContextPayload(BaseModel):
    input_data: InputData
    intermediate_results: Dict[str, Any] = {}
    error_log: List[ErrorLogEntry] = []


class FlightPlan(BaseModel):
    """
    The Flight Plan — the core execution artifact of BIAS.
    Created by Orchestrator. Travels with every claim request.
    Every service reads this, updates its stage, and passes it on.
    """
    flight_plan_metadata: FlightPlanMetadata
    execution_state: ExecutionState
    service_registry: ServiceRegistry
    steps: List[FlightPlanStep]
    context_payload: ContextPayload
