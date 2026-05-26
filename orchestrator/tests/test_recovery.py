"""
Tests for Stage 99 recovery logic.
"""
import pytest

from shared.models.flight_plan import OverallStatusEnum, StageStatusEnum
from shared.models.flight_plan import RequestTypeEnum
from shared.models.flight_plan import ServiceRegistry as FPServiceRegistry
from orchestrator.agent.orchestrator_agent import OrchestratorAgent


def make_registry() -> FPServiceRegistry:
    return FPServiceRegistry(
        ORCHESTRATOR="http://orchestrator:8001",
        COMMUNICATOR="http://communicator:8000",
        FILE_MANAGEMENT="http://file-management:8002",
        DB_AGENT="http://db-agent:8003",
        CLAIMS_EXPERT="http://claims-expert:8004",
        LLM_AGENT="http://llm-agent:8005",
        CHATBOT="http://chatbot:8006",
    )


def test_failed_stage_routes_to_99():
    """Every step's failure routing should point to stage 99."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-RECOVERY",
        member_id="MBR-RECOVERY",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    for step in plan.steps:
        assert step.routing.next_on_failure == 99


def test_plan_initial_stage_is_pending():
    """All stages should start as PENDING."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-PENDING",
        member_id="MBR-PENDING",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    for step in plan.steps:
        assert step.status == StageStatusEnum.PENDING
