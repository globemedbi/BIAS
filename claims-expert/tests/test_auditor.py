"""
Tests for the claims auditor decision logic.
"""
import pytest

from claims_expert.auditor.auditor import determine_decision, AuditDecision, DiscrepancySeverity


def test_approved_no_discrepancies():
    """within_policy + no discrepancies = APPROVED."""
    decision = determine_decision(within_policy=True, discrepancies=[])
    assert decision == AuditDecision.APPROVED


def test_approved_low_discrepancies_only():
    """within_policy + only LOW discrepancies = APPROVED."""
    discrepancies = [{"field": "amount", "severity": DiscrepancySeverity.LOW}]
    decision = determine_decision(within_policy=True, discrepancies=discrepancies)
    assert decision == AuditDecision.APPROVED


def test_pending_review_medium_discrepancy():
    """within_policy + MEDIUM discrepancy = PENDING_REVIEW."""
    discrepancies = [{"field": "procedure", "severity": DiscrepancySeverity.MEDIUM}]
    decision = determine_decision(within_policy=True, discrepancies=discrepancies)
    assert decision == AuditDecision.PENDING_REVIEW


def test_rejected_high_discrepancy():
    """within_policy + HIGH discrepancy = REJECTED."""
    discrepancies = [{"field": "diagnosis", "severity": DiscrepancySeverity.HIGH}]
    decision = determine_decision(within_policy=True, discrepancies=discrepancies)
    assert decision == AuditDecision.REJECTED


def test_rejected_out_of_policy():
    """out of policy regardless of discrepancies = REJECTED."""
    decision = determine_decision(within_policy=False, discrepancies=[])
    assert decision == AuditDecision.REJECTED
