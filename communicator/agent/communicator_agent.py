"""
Communicator Agent — orchestrates the external-facing claim submission flow.
"""
from typing import Any, Dict, Optional

from shared.communication_layer.logger import get_logger
from shared.models.claim import Claim

logger = get_logger("COMMUNICATOR")

# In-memory session store for Phase 1
# Key: request_id, Value: {plan_id, claim_id, status, result}
_session_store: Dict[str, Dict[str, Any]] = {}


class CommunicatorAgent:
    """Manages claim sessions and coordinates with the Orchestrator."""

    def store_session(self, request_id: str, plan_id: str, claim_id: str) -> None:
        """Stores a new claim session after plan creation."""
        _session_store[request_id] = {
            "plan_id": plan_id,
            "claim_id": claim_id,
            "status": "IN_PROGRESS",
            "result": None,
        }
        logger.info("session_stored", request_id=request_id, plan_id=plan_id)

    def get_session(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a session by request_id."""
        return _session_store.get(request_id)

    def update_session_result(self, request_id: str, result: Dict[str, Any]) -> None:
        """Updates a session with the final result from Chatbot callback."""
        if request_id in _session_store:
            _session_store[request_id]["status"] = "COMPLETED"
            _session_store[request_id]["result"] = result
            logger.info("session_result_stored", request_id=request_id)
