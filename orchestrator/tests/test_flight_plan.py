"""
Tests for Flight Plan creation logic.
"""
import pytest

from shared.models.flight_plan import RequestTypeEnum, OverallStatusEnum
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


def test_create_claim_audit_plan_has_three_stages():
    """CLAIM_AUDIT plan should have exactly 3 stages."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-001",
        member_id="MBR-001",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=["s3://bucket/file.pdf"],
        service_registry=make_registry(),
    )
    assert len(plan.steps) == 3
    assert plan.execution_state.total_stages == 3


def test_create_doc_anonymization_plan_has_one_stage():
    """DOC_ANONYMIZATION plan should have exactly 1 stage."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-002",
        member_id="MBR-002",
        request_type=RequestTypeEnum.DOC_ANONYMIZATION,
        file_uris=["s3://bucket/doc.pdf"],
        service_registry=make_registry(),
    )
    assert len(plan.steps) == 1


def test_plan_starts_in_progress():
    """New plans should have IN_PROGRESS overall status."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-003",
        member_id="MBR-003",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    assert plan.execution_state.overall_status == OverallStatusEnum.IN_PROGRESS


def test_plan_has_unique_ids():
    """Each plan should have a unique plan_id and request_id."""
    agent = OrchestratorAgent()
    plan1 = agent.create_plan(
        claim_id="CLM-004",
        member_id="MBR-004",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    plan2 = agent.create_plan(
        claim_id="CLM-005",
        member_id="MBR-005",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    assert plan1.flight_plan_metadata.plan_id != plan2.flight_plan_metadata.plan_id


def test_claim_audit_last_stage_routes_to_complete():
    """Last stage of CLAIM_AUDIT should route to COMPLETE."""
    agent = OrchestratorAgent()
    plan = agent.create_plan(
        claim_id="CLM-006",
        member_id="MBR-006",
        request_type=RequestTypeEnum.CLAIM_AUDIT,
        file_uris=[],
        service_registry=make_registry(),
    )
    last_step = plan.steps[-1]
    assert last_step.routing.next_on_success == "COMPLETE"
