"""
Legacy DB connector — connects to the on-premise PostgreSQL database.
"""
import os
from typing import Any, Dict, List, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("DB_AGENT")

LEGACY_DB_URL = os.getenv("LEGACY_DB_URL", "")


class LegacyDBConnector:
    """Handles all queries to the legacy PostgreSQL database."""

    async def fetch_claim(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Fetches a single claim record by claim_id."""
        raise NotImplementedError

    async def fetch_member_history(self, member_id: str) -> List[Dict[str, Any]]:
        """Returns all historical claims for a member."""
        raise NotImplementedError

    async def fetch_authorization(self, claim_id: str) -> Optional[Dict[str, Any]]:
        """Fetches the authorization and coverage record for a claim."""
        raise NotImplementedError

    async def store_ocr_result(self, claim_id: str, ocr_data: Dict[str, Any]) -> bool:
        """Stores an OCR extraction result."""
        raise NotImplementedError
