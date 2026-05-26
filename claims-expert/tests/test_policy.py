"""
Tests for medical policy rules.
"""
import pytest

from claims_expert.medical_logic.medical_rules import is_within_policy


def test_is_within_policy_raises_not_implemented():
    """is_within_policy should raise NotImplementedError until implemented."""
    with pytest.raises(NotImplementedError):
        is_within_policy(["CPT-99213"], ["Z00.00"])
