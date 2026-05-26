"""
Chatbot chat routes.
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from shared.communication_layer.logger import get_logger
from shared.models.response import SuccessResponse

logger = get_logger("CHATBOT")
router = APIRouter()


class ChatRequest(BaseModel):
    session_id: str
    message: str
    user_id: str
    user_type: str = "MEMBER"


class CreateSessionRequest(BaseModel):
    user_id: str
    user_type: str = "MEMBER"


@router.post("/chat")
async def chat(request: ChatRequest) -> SuccessResponse:
    """Handles a real-time chat message from a user."""
    logger.info("chat_message_received", session_id=request.session_id, user_type=request.user_type)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str) -> SuccessResponse:
    """Returns conversation history for a session."""
    logger.info("chat_history_requested", session_id=session_id)
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/chat/session")
async def create_session(request: CreateSessionRequest) -> SuccessResponse:
    """Creates a new conversation session."""
    session_id = str(uuid.uuid4())
    logger.info("session_created", session_id=session_id, user_id=request.user_id)
    return SuccessResponse(service="CHATBOT", data={"session_id": session_id})
