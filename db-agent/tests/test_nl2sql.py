"""
Tests for NL2SQL safety validation.
"""
import pytest

from db_agent.nl2sql.translator import is_safe_query


def test_select_query_is_safe():
    """A plain SELECT query should pass the safety check."""
    assert is_safe_query("SELECT claim_id FROM claims WHERE member_id = '123'") is True


def test_delete_query_is_blocked():
    """DELETE queries must be blocked."""
    assert is_safe_query("DELETE FROM claims WHERE 1=1") is False


def test_drop_table_is_blocked():
    """DROP TABLE must be blocked."""
    assert is_safe_query("DROP TABLE members") is False


def test_update_is_blocked():
    """UPDATE statements must be blocked."""
    assert is_safe_query("UPDATE claims SET status = 'APPROVED'") is False


def test_case_insensitive_blocking():
    """Blocking must be case-insensitive."""
    assert is_safe_query("DeLeTe FROM claims") is False
    assert is_safe_query("INSERT INTO claims VALUES (1)") is False
