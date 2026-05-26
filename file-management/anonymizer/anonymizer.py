"""
Anonymizer client — removes PII from OCR-extracted text.
MUST be called before any translation or external processing.
"""
import os
from typing import Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("FILE_MANAGEMENT")

ANONYMIZER_URL = os.getenv("ANONYMIZER_URL", "http://anonymizer:8090")
ANONYMIZER_API_KEY = os.getenv("ANONYMIZER_API_KEY", "")


class Anonymizer:
    """Client for the PII anonymization service."""

    async def anonymize(self, text: str) -> Optional[str]:
        """
        Removes PII from text. Returns anonymized text or None on failure.
        Pipeline MUST stop if this returns None.
        """
        raise NotImplementedError
