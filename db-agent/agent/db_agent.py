"""
DB Agent — routes data requests to the correct database connector.
"""
from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")


class DBAgent:
    """Routes data operations to the appropriate database connector."""

    def validate_service_token(self, token: str, service_name: str) -> bool:
        """Validates that the calling service has a valid internal token."""
        import os
        expected = os.getenv("INTERNAL_SERVICE_TOKEN", "")
        if not expected or token != expected:
            logger.warning("invalid_service_token", service=service_name)
            return False
        return True
