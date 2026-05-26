"""
Tests for the claims reconciler.
"""
import pytest

from claims_expert.reconciler.reconciler import Reconciler


def test_reconciler_raises_not_implemented():
    """reconcile should raise NotImplementedError until implemented."""
    reconciler = Reconciler()
    with pytest.raises(NotImplementedError):
        reconciler.reconcile(
            ocr_data={"procedure": "CPT-99213"},
            auth_record={"authorized_procedure": "CPT-99212"},
        )
