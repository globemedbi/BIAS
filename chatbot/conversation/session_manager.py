"""
Session manager — manages in-memory conversation sessions with TTL.
"""
import os
import time
from typing import Any, Dict, List, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("CHATBOT")

SESSION_TTL_HOURS = int(os.getenv("SESSION_TTL_HOURS", "24"))
SESSION_TTL_SECONDS = SESSION_TTL_HOURS * 3600

_sessions: Dict[str, Dict[str, Any]] = {}


def create_session(session_id: str, user_id: str, user_type: str) -> None:
    """Creates a new conversation session."""
    _sessions[session_id] = {
        "user_id": user_id,
        "user_type": user_type,
        "messages": [],
        "context": {},
        "created_at": time.time(),
    }
    logger.info("session_created", session_id=session_id, user_type=user_type)


def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Returns a session if it exists and has not expired."""
    session = _sessions.get(session_id)
    if not session:
        return None
    if time.time() - session["created_at"] > SESSION_TTL_SECONDS:
        del _sessions[session_id]
        logger.info("session_expired", session_id=session_id)
        return None
    return session


def append_message(session_id: str, role: str, content: str) -> None:
    """Appends a message to a session. Never logs content (may contain PII)."""
    session = get_session(session_id)
    if session:
        session["messages"].append({"role": role, "content": content})
