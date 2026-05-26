"""
Prompt builder — assembles system + user prompts from templates.
"""
from pathlib import Path
from typing import Optional

TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_system_prompt(task_type: str) -> str:
    """Loads the system prompt template for a given task type."""
    template_path = TEMPLATES_DIR / f"{task_type}.txt"
    if not template_path.exists():
        raise ValueError(f"No template for task_type: {task_type}")
    return template_path.read_text(encoding="utf-8")


def build_prompt(task_type: str, context: str, user_input: str) -> dict:
    """
    Builds a messages array for the LLM API call.
    Returns {"system": str, "user": str}.
    """
    system_prompt = load_system_prompt(task_type)
    user_message = f"{context}\n\n{user_input}".strip() if context else user_input
    return {"system": system_prompt, "user": user_message}
