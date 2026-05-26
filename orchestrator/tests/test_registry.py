"""
Tests for the service registry.
"""
import pytest

from orchestrator.service_registry.registry import ServiceRegistry


def test_register_and_get_url():
    """Registered service URL should be retrievable."""
    registry = ServiceRegistry()
    registry.register("DB_AGENT", "http://db-agent", 8003)
    assert registry.get_url("DB_AGENT") == "http://db-agent"


def test_get_url_returns_none_for_unknown():
    """Unknown service should return None."""
    registry = ServiceRegistry()
    assert registry.get_url("UNKNOWN_SERVICE") is None


def test_mark_unhealthy_then_healthy():
    """Service health toggle should work correctly."""
    registry = ServiceRegistry()
    registry.register("LLM_AGENT", "http://llm-agent", 8005)
    registry.mark_unhealthy("LLM_AGENT")
    entries = registry.all_entries()
    assert entries["LLM_AGENT"]["healthy"] is False
    registry.mark_healthy("LLM_AGENT")
    entries = registry.all_entries()
    assert entries["LLM_AGENT"]["healthy"] is True


def test_all_entries_returns_registered_services():
    """all_entries should return all registered services."""
    registry = ServiceRegistry()
    registry.register("ORCHESTRATOR", "http://orchestrator", 8001)
    registry.register("COMMUNICATOR", "http://communicator", 8000)
    entries = registry.all_entries()
    assert "ORCHESTRATOR" in entries
    assert "COMMUNICATOR" in entries
