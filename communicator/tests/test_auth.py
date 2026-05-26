"""
Tests for JWT validation logic.
"""
import pytest
from unittest.mock import patch

from communicator.auth.jwt_validator import extract_bearer_token, validate_token


def test_extract_bearer_token_valid():
    """Should extract token from valid Bearer header."""
    token = extract_bearer_token("Bearer mytoken123")
    assert token == "mytoken123"


def test_extract_bearer_token_none_header():
    """Should return None for missing header."""
    assert extract_bearer_token(None) is None


def test_extract_bearer_token_invalid_format():
    """Should return None for malformed header."""
    assert extract_bearer_token("Token mytoken") is None
    assert extract_bearer_token("mytoken") is None


def test_validate_token_invalid_returns_none():
    """Invalid token should return None without raising."""
    result = validate_token("invalid.token.here")
    assert result is None
