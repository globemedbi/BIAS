"""
Tests for session manager.
"""
import pytest
import time
from unittest.mock import patch

from chatbot.conversation.session_manager import create_session, get_session, append_message


def test_create_and_get_session():
    """Created session should be retrievable."""
    create_session("sess-001", "user-001", "MEMBER")
    session = get_session("sess-001")
    assert session is not None
    assert session["user_type"] == "MEMBER"
    assert session["user_id"] == "user-001"


def test_get_nonexistent_session():
    """Unknown session_id should return None."""
    assert get_session("does-not-exist") is None


def test_append_message():
    """Messages should be appended to session."""
    create_session("sess-002", "user-002", "ADJUSTER")
    append_message("sess-002", "user", "What is the status?")
    session = get_session("sess-002")
    assert len(session["messages"]) == 1
    assert session["messages"][0]["role"] == "user"


def test_session_expires():
    """Sessions beyond TTL should return None."""
    create_session("sess-expire", "user-expire", "MEMBER")
    with patch("chatbot.conversation.session_manager.SESSION_TTL_SECONDS", -1):
        result = get_session("sess-expire")
        assert result is None
