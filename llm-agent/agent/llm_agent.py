"""
LLM Agent — orchestrates prompt building, model routing, and provider calls.
"""
from shared.communication_layer.logger import get_logger

logger = get_logger("LLM_AGENT")


class LLMAgent:
    """Core agent that coordinates prompt building and model selection."""

    def sanitize_prompt(self, text: str) -> str:
        """
        Removes potential prompt injection patterns from input text.
        This is a baseline implementation — extend for production.
        """
        injection_patterns = [
            "ignore previous instructions",
            "disregard all prior",
            "forget your instructions",
            "system prompt:",
            "new instructions:",
        ]
        sanitized = text
        for pattern in injection_patterns:
            sanitized = sanitized.lower().replace(pattern.lower(), "[REMOVED]")
        return sanitized
