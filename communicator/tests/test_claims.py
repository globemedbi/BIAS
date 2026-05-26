"""
Tests for the Communicator session management.
"""
import pytest

from communicator.agent.communicator_agent import CommunicatorAgent


def test_store_and_get_session():
    """Stored session should be retrievable by request_id."""
    agent = CommunicatorAgent()
    agent.store_session("req-001", "plan-001", "clm-001")
    session = agent.get_session("req-001")
    assert session is not None
    assert session["plan_id"] == "plan-001"
    assert session["status"] == "IN_PROGRESS"


def test_get_session_unknown_returns_none():
    """Unknown request_id should return None."""
    agent = CommunicatorAgent()
    assert agent.get_session("unknown-request") is None


def test_update_session_result():
    """Updating session result should set status to COMPLETED."""
    agent = CommunicatorAgent()
    agent.store_session("req-002", "plan-002", "clm-002")
    agent.update_session_result("req-002", {"decision": "APPROVED"})
    session = agent.get_session("req-002")
    assert session["status"] == "COMPLETED"
    assert session["result"]["decision"] == "APPROVED"
