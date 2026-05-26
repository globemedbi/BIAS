"""
Tests for the prompt builder.
"""
import pytest

from llm_agent.prompt_engine.prompt_builder import build_prompt, load_system_prompt


def test_load_system_prompt_summarize():
    """Should load the summarize template without error."""
    prompt = load_system_prompt("summarize")
    assert len(prompt) > 0


def test_load_system_prompt_audit():
    """Should load the audit template without error."""
    prompt = load_system_prompt("audit")
    assert "discrepanc" in prompt.lower()


def test_load_unknown_task_type_raises():
    """Unknown task_type should raise ValueError."""
    with pytest.raises(ValueError):
        load_system_prompt("nonexistent_task")


def test_build_prompt_with_context():
    """build_prompt should combine context and input."""
    result = build_prompt("chat", "member context here", "What is my status?")
    assert "member context here" in result["user"]
    assert "What is my status?" in result["user"]


def test_build_prompt_without_context():
    """build_prompt should use just input when context is empty."""
    result = build_prompt("chat", "", "Hello?")
    assert result["user"] == "Hello?"
