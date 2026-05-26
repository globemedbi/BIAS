"""
Claims Agent — orchestrates the audit workflow.
"""
from shared.communication_layer.logger import get_logger
from shared.models.flight_plan import FlightPlan

logger = get_logger("CLAIMS_EXPERT")


class ClaimsAgent:
    """Coordinates the full audit pipeline for a claim."""

    async def run_audit(self, flight_plan: FlightPlan) -> dict:
        """
        Executes the full audit:
        1. Fetch OCR text from File Management
        2. Fetch authorization from DB Agent
        3. Fetch claim history from DB Agent
        4. Call LLM Agent to summarize
        5. Call LLM Agent to reconcile
        6. Determine decision
        7. Generate Master Summary
        8. Hand off to Chatbot
        """
        raise NotImplementedError
