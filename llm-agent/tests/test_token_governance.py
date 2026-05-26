"""
Tests for token governance.
"""
import pytest

from llm_agent.token_governance.governor import record_usage, get_usage_report, reset_usage


def test_record_and_get_usage():
    """Recorded tokens should appear in the usage report."""
    reset_usage("TEST_SERVICE")
    record_usage("TEST_SERVICE", 100)
    report = get_usage_report()
    assert report.get("TEST_SERVICE", 0) >= 100


def test_usage_accumulates():
    """Multiple calls should accumulate token counts."""
    reset_usage("ACCUMULATE_SERVICE")
    record_usage("ACCUMULATE_SERVICE", 50)
    record_usage("ACCUMULATE_SERVICE", 75)
    report = get_usage_report()
    assert report["ACCUMULATE_SERVICE"] == 125


def test_reset_clears_usage():
    """reset_usage should zero out the counter for that service."""
    record_usage("RESET_SERVICE", 200)
    reset_usage("RESET_SERVICE")
    report = get_usage_report()
    assert report.get("RESET_SERVICE", 0) == 0
