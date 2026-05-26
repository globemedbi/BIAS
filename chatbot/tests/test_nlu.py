"""
Tests for NLU intent classifier.
"""
import pytest

from chatbot.nlu.intent_classifier import Intent, INTENT_ROUTING


def test_all_intents_have_routing():
    """Every Intent enum value should have a routing entry."""
    for intent in Intent:
        assert intent in INTENT_ROUTING, f"Missing routing for intent: {intent}"


def test_routing_entries_have_service_and_endpoint():
    """Each routing entry must have both service and endpoint."""
    for intent, routing in INTENT_ROUTING.items():
        assert "service" in routing, f"Missing service for {intent}"
        assert "endpoint" in routing, f"Missing endpoint for {intent}"
