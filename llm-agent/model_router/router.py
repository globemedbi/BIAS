"""
LLM Agent model router — selects the appropriate model and provider.
"""
import os
from enum import Enum
from typing import Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("LLM_AGENT")


class ModelPreference(str, Enum):
    FAST = "FAST"
    BALANCED = "BALANCED"
    POWERFUL = "POWERFUL"


TASK_TYPE_OVERRIDES = {
    "audit": ModelPreference.POWERFUL,
    "reconcile": ModelPreference.POWERFUL,
    "summarize": ModelPreference.BALANCED,
    "extract": ModelPreference.BALANCED,
    "chat": ModelPreference.FAST,
}


def select_model(task_type: str, model_preference: ModelPreference) -> str:
    """
    Selects the model identifier to use.
    task_type overrides model_preference when there is a conflict.
    """
    effective_preference = TASK_TYPE_OVERRIDES.get(task_type, model_preference)

    model_map = {
        ModelPreference.FAST: os.getenv("DEFAULT_MODEL_FAST", "gpt-3.5-turbo"),
        ModelPreference.BALANCED: os.getenv("DEFAULT_MODEL_BALANCED", "gpt-4o-mini"),
        ModelPreference.POWERFUL: os.getenv("DEFAULT_MODEL_POWERFUL", "claude-sonnet-4-20250514"),
    }
    selected = model_map[effective_preference]
    logger.info("model_selected", task_type=task_type, model=selected)
    return selected
