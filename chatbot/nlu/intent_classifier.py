"""
NLU intent classifier — classifies user messages to route them correctly.
"""
from enum import Enum
from typing import Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("CHATBOT")


class Intent(str, Enum):
    STATUS_CHECK = "STATUS_CHECK"
    HISTORY_QUERY = "HISTORY_QUERY"
    POLICY_QUERY = "POLICY_QUERY"
    DOCUMENT_REQUEST = "DOCUMENT_REQUEST"
    GENERAL_QUESTION = "GENERAL_QUESTION"


INTENT_ROUTING = {
    Intent.STATUS_CHECK: {"service": "ORCHESTRATOR", "endpoint": "/plan/{plan_id}/status"},
    Intent.HISTORY_QUERY: {"service": "DB_AGENT", "endpoint": "/claims/history"},
    Intent.POLICY_QUERY: {"service": "CLAIMS_EXPERT", "endpoint": "/api/v1/validate/policy"},
    Intent.DOCUMENT_REQUEST: {"service": "FILE_MANAGEMENT", "endpoint": "/api/v1/extract/{claim_id}"},
    Intent.GENERAL_QUESTION: {"service": "LLM_AGENT", "endpoint": "/api/v1/complete"},
}


async def classify_intent(message: str, user_type: str) -> Intent:
    """
    Classifies a user message into an Intent.
    Calls LLM Agent for classification.
    """
    raise NotImplementedError
