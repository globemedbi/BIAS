"""
Tests for DB Agent service token validation and NL2SQL safety.
"""
import pytest
from unittest.mock import patch
import os

from db_agent.agent.db_agent import DBAgent
from db_agent.nl2sql.translator import is_safe_query, BLOCKED_KEYWORDS


def test_valid_service_token():
    """Valid internal token should pass validation."""
    with patch.dict(os.environ, {"INTERNAL_SERVICE_TOKEN": "valid-token-here"}):
        agent = DBAgent()
        assert agent.validate_service_token("valid-token-here", "CLAIMS_EXPERT") is True


def test_invalid_service_token():
    """Wrong token should fail validation."""
    with patch.dict(os.environ, {"INTERNAL_SERVICE_TOKEN": "correct-token"}):
        agent = DBAgent()
        assert agent.validate_service_token("wrong-token", "CLAIMS_EXPERT") is False
