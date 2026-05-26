"""
Tests for the response formatter.
"""
import pytest

from chatbot.formatter.response_formatter import format_for_member, format_for_adjuster, format_for_admin


def test_format_member_approved():
    """APPROVED decision should produce positive member message."""
    result = format_for_member({"decision": "APPROVED"})
    assert "approved" in result.lower()


def test_format_member_rejected():
    """REJECTED decision should produce sympathetic member message."""
    result = format_for_member({"decision": "REJECTED"})
    assert "not" in result.lower() or "unfortunately" in result.lower()


def test_format_adjuster_includes_discrepancies():
    """Adjuster format should include discrepancy details."""
    result = format_for_adjuster({
        "decision": "PENDING_REVIEW",
        "discrepancies": [
            {"field": "amount", "severity": "MEDIUM", "ocr_value": "500", "auth_value": "400"}
        ]
    })
    assert "MEDIUM" in result
    assert "amount" in result


def test_format_admin_is_json():
    """Admin format should be valid JSON."""
    import json
    result = format_for_admin({"decision": "APPROVED", "plan_id": "p-123"})
    parsed = json.loads(result)
    assert parsed["decision"] == "APPROVED"
