"""
Orchestrator Agent — core logic for Flight Plan creation and recovery.
"""
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import (
    ContextPayload,
    ExecutionState,
    FlightPlan,
    FlightPlanMetadata,
    FlightPlanStep,
    InputData,
    OverallStatusEnum,
    RequestTypeEnum,
    ServiceRegistry,
    StageStatusEnum,
    StepRouting,
)

logger = get_logger("ORCHESTRATOR")


class OrchestratorAgent:
    """Creates and manages Flight Plans for claim processing requests."""

    def create_plan(
        self,
        claim_id: str,
        member_id: str,
        request_type: RequestTypeEnum,
        file_uris: List[str],
        service_registry: ServiceRegistry,
    ) -> FlightPlan:
        """Creates a Flight Plan from the appropriate business template."""
        plan_id = str(uuid.uuid4())
        request_id = str(uuid.uuid4())

        steps = self._load_template_steps(request_type)

        plan = FlightPlan(
            flight_plan_metadata=FlightPlanMetadata(
                plan_id=plan_id,
                request_id=request_id,
                request_type=request_type,
                created_at=datetime.utcnow(),
            ),
            execution_state=ExecutionState(
                overall_status=OverallStatusEnum.IN_PROGRESS,
                current_stage=0,
                total_stages=len(steps),
            ),
            service_registry=service_registry,
            steps=steps,
            context_payload=ContextPayload(
                input_data=InputData(
                    claim_id=claim_id,
                    member_id=member_id,
                    file_uris=file_uris,
                ),
            ),
        )

        logger.info(
            "flight_plan_created",
            plan_id=plan_id,
            claim_id=claim_id,
            request_type=request_type.value,
            total_stages=len(steps),
        )
        return plan

    def _load_template_steps(self, request_type: RequestTypeEnum) -> List[FlightPlanStep]:
        """Returns the step list for a given request type."""
        if request_type == RequestTypeEnum.CLAIM_AUDIT:
            return [
                FlightPlanStep(
                    stage=1,
                    service="FILE_MANAGEMENT",
                    endpoint="/api/v1/process",
                    routing=StepRouting(next_on_success=2, next_on_failure=99),
                ),
                FlightPlanStep(
                    stage=2,
                    service="CLAIMS_EXPERT",
                    endpoint="/api/v1/audit",
                    routing=StepRouting(next_on_success=3, next_on_failure=99),
                ),
                FlightPlanStep(
                    stage=3,
                    service="CHATBOT",
                    endpoint="/api/v1/format",
                    routing=StepRouting(next_on_success="COMPLETE", next_on_failure=99),
                ),
            ]
        if request_type == RequestTypeEnum.DOC_ANONYMIZATION:
            return [
                FlightPlanStep(
                    stage=1,
                    service="FILE_MANAGEMENT",
                    endpoint="/api/v1/process",
                    routing=StepRouting(next_on_success="COMPLETE", next_on_failure=99),
                ),
            ]
        # CLAIM_STATUS
        return [
            FlightPlanStep(
                stage=1,
                service="CHATBOT",
                endpoint="/api/v1/chat",
                routing=StepRouting(next_on_success="COMPLETE", next_on_failure=99),
            ),
        ]
