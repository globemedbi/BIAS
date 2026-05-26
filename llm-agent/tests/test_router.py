"""
Tests for the LLM model router.
"""
import pytest
from unittest.mock import patch
import os

from llm_agent.model_router.router import select_model, ModelPreference


def test_select_model_fast():
    """FAST preference should return the fast model."""
    with patch.dict(os.environ, {"DEFAULT_MODEL_FAST": "gpt-3.5-turbo"}):
        model = select_model("chat", ModelPreference.FAST)
        assert model == "gpt-3.5-turbo"


def test_select_model_powerful():
    """POWERFUL preference should return the powerful model."""
    with patch.dict(os.environ, {"DEFAULT_MODEL_POWERFUL": "claude-sonnet-4-20250514"}):
        model = select_model("chat", ModelPreference.POWERFUL)
        assert model == "claude-sonnet-4-20250514"


def test_task_type_overrides_preference():
    """audit task_type should always use POWERFUL regardless of preference."""
    with patch.dict(os.environ, {"DEFAULT_MODEL_POWERFUL": "claude-sonnet-4-20250514"}):
        model = select_model("audit", ModelPreference.FAST)
        assert model == "claude-sonnet-4-20250514"


def test_reconcile_uses_powerful():
    """reconcile task_type should use POWERFUL model."""
    with patch.dict(os.environ, {"DEFAULT_MODEL_POWERFUL": "claude-sonnet-4-20250514"}):
        model = select_model("reconcile", ModelPreference.BALANCED)
        assert model == "claude-sonnet-4-20250514"
