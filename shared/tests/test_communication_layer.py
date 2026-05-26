"""
Tests for the BIAS shared communication layer.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from shared.models.flight_plan import (
    FlightPlan,
    FlightPlanMetadata,
    FlightPlanStep,
    ExecutionState,
    ServiceRegistry,
    ContextPayload,
    InputData,
    StepRouting,
    StageStatusEnum,
    OverallStatusEnum,
    RequestTypeEnum,
)
from shared.communication_layer.flight_plan_reader import (
    get_current_step,
    get_step_by_stage,
    mark_stage_in_progress,
    get_intermediate_result,
    set_intermediate_result,
)


def make_flight_plan() -> FlightPlan:
    """Creates a minimal test Flight Plan."""
    return FlightPlan(
        flight_plan_metadata=FlightPlanMetadata(
            plan_id="test-plan-id",
            request_id="test-request-id",
            request_type=RequestTypeEnum.CLAIM_AUDIT,
        ),
        execution_state=ExecutionState(
            overall_status=OverallStatusEnum.IN_PROGRESS,
            current_stage=1,
            total_stages=3,
        ),
        service_registry=ServiceRegistry(
            ORCHESTRATOR="http://orchestrator:8001",
            COMMUNICATOR="http://communicator:8000",
            FILE_MANAGEMENT="http://file-management:8002",
            DB_AGENT="http://db-agent:8003",
            CLAIMS_EXPERT="http://claims-expert:8004",
            LLM_AGENT="http://llm-agent:8005",
            CHATBOT="http://chatbot:8006",
        ),
        steps=[
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
                routing=StepRouting(next_on_success="COMPLETE", next_on_failure=99),
            ),
        ],
        context_payload=ContextPayload(
            input_data=InputData(claim_id="CLM-001", member_id="MBR-001"),
        ),
    )


def test_get_current_step_returns_matching_stage():
    """get_current_step should return the step for current_stage."""
    fp = make_flight_plan()
    step = get_current_step(fp)
    assert step is not None
    assert step.stage == 1
    assert step.service == "FILE_MANAGEMENT"


def test_get_step_by_stage_returns_correct_step():
    """get_step_by_stage should return step for the given stage number."""
    fp = make_flight_plan()
    step = get_step_by_stage(fp, 2)
    assert step is not None
    assert step.service == "CLAIMS_EXPERT"


def test_get_step_by_stage_returns_none_for_missing():
    """get_step_by_stage should return None for a nonexistent stage."""
    fp = make_flight_plan()
    step = get_step_by_stage(fp, 99)
    assert step is None


def test_mark_stage_in_progress_updates_status_and_current():
    """mark_stage_in_progress should set step status and execution state."""
    fp = make_flight_plan()
    mark_stage_in_progress(fp, 2)
    step = get_step_by_stage(fp, 2)
    assert step is not None
    assert step.status == StageStatusEnum.IN_PROGRESS
    assert fp.execution_state.current_stage == 2


def test_intermediate_results_roundtrip():
    """set/get intermediate result should store and retrieve values."""
    fp = make_flight_plan()
    set_intermediate_result(fp, "ocr_text", "extracted text content")
    result = get_intermediate_result(fp, "ocr_text")
    assert result == "extracted text content"


def test_get_intermediate_result_returns_none_for_missing():
    """get_intermediate_result returns None for unknown keys."""
    fp = make_flight_plan()
    result = get_intermediate_result(fp, "nonexistent_key")
    assert result is None
