"""
BIAS Flight Plan Hand-off
Handles reading the next stage from a Flight Plan
and making the API call to the next service.
"""
from typing import Any, Dict, Optional

import httpx
import structlog

from shared.models.flight_plan import FlightPlan, StageStatusEnum

logger = structlog.get_logger()

TIMEOUT_SECONDS = 30.0


async def execute_hand_off(
    flight_plan: FlightPlan,
    completed_stage: int,
    output_uri: Optional[str] = None,
    additional_payload: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Commits the current stage and hands off to the next service.

    CRITICAL ORDER:
    1. Mark current stage as COMPLETED in flight plan
    2. Determine next stage from routing
    3. Look up next service URL from registry
    4. POST to next service with updated flight plan
    5. Return success/failure

    Args:
        flight_plan: The current Flight Plan
        completed_stage: The stage number just completed
        output_uri: Optional S3 URI of output artifact
        additional_payload: Optional extra data for next service

    Returns:
        True if hand-off succeeded, False if failed
    """
    # Step 1: Update current stage status
    for step in flight_plan.steps:
        if step.stage == completed_stage:
            step.status = StageStatusEnum.COMPLETED
            if output_uri:
                step.output_uri = output_uri
            break

    # Step 2: Find next stage
    current_step = next(
        (s for s in flight_plan.steps if s.stage == completed_stage), None
    )
    if not current_step:
        logger.error("stage_not_found", stage=completed_stage)
        return False

    next_stage = current_step.routing.next_on_success
    if next_stage == "COMPLETE":
        logger.info("flight_plan_complete", plan_id=flight_plan.flight_plan_metadata.plan_id)
        return True

    # Step 3: Find next step definition
    next_step = next(
        (s for s in flight_plan.steps if s.stage == next_stage), None
    )
    if not next_step:
        logger.error("next_stage_not_found", next_stage=next_stage)
        return False

    # Step 4: Look up service URL
    registry = flight_plan.service_registry
    service_url = getattr(registry, next_step.service, None)
    if not service_url:
        logger.error("service_not_in_registry", service=next_step.service)
        return False

    # Step 5: POST to next service
    target_url = f"{service_url}{next_step.endpoint}"
    payload = {
        "flight_plan": flight_plan.model_dump(),
        **(additional_payload or {}),
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(target_url, json=payload)
            response.raise_for_status()
            logger.info(
                "hand_off_success",
                from_stage=completed_stage,
                to_stage=next_stage,
                service=next_step.service,
                url=target_url,
            )
            return True
    except Exception as e:
        logger.error(
            "hand_off_failed",
            from_stage=completed_stage,
            to_stage=next_stage,
            service=next_step.service,
            error=str(e),
        )
        return False
