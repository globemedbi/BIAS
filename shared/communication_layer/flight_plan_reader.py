"""
BIAS Flight Plan Reader
Utilities for reading and validating Flight Plan objects.
"""
import json
from pathlib import Path
from typing import Any, Dict, Optional

import structlog

from shared.models.flight_plan import FlightPlan, FlightPlanStep, StageStatusEnum

logger = structlog.get_logger()

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "flight_plan_v1.json"


def get_current_step(flight_plan: FlightPlan) -> Optional[FlightPlanStep]:
    """Returns the step matching the current execution stage."""
    current_stage = flight_plan.execution_state.current_stage
    return next(
        (s for s in flight_plan.steps if s.stage == current_stage), None
    )


def get_step_by_stage(flight_plan: FlightPlan, stage: int) -> Optional[FlightPlanStep]:
    """Returns the step for a given stage number."""
    return next((s for s in flight_plan.steps if s.stage == stage), None)


def mark_stage_in_progress(flight_plan: FlightPlan, stage: int) -> None:
    """Marks a stage as IN_PROGRESS and updates current_stage."""
    for step in flight_plan.steps:
        if step.stage == stage:
            step.status = StageStatusEnum.IN_PROGRESS
            break
    flight_plan.execution_state.current_stage = stage


def get_intermediate_result(flight_plan: FlightPlan, key: str) -> Any:
    """Retrieves a value from the intermediate_results context."""
    return flight_plan.context_payload.intermediate_results.get(key)


def set_intermediate_result(flight_plan: FlightPlan, key: str, value: Any) -> None:
    """Stores a value in the intermediate_results context."""
    flight_plan.context_payload.intermediate_results[key] = value
