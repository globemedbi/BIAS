"""
Chatbot Agent — coordinates formatting and conversation handling.
"""
from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan

logger = get_logger("CHATBOT")


class ChatbotAgent:
    """Orchestrates result formatting and user interaction."""

    async def format_and_deliver(
        self,
        flight_plan: FlightPlan,
        audit_result: dict,
        user_type: str,
    ) -> dict:
        """
        Formats the audit result for the user_type and triggers callback to Communicator.
        """
        raise NotImplementedError
