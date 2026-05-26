"""
OCR engine client — calls the external OCR service.
"""
import os
from typing import Optional

import httpx

from shared.communication_layer.logger import get_logger

logger = get_logger("FILE_MANAGEMENT")

OCR_ENGINE_URL = os.getenv("OCR_ENGINE_URL", "http://ocr-engine:8080")


class OCREngine:
    """Client for the external OCR engine."""

    async def extract_text(self, file_uri: str) -> Optional[str]:
        """
        Sends a file URI to the OCR engine and returns extracted text.
        Returns None if OCR fails.
        """
        raise NotImplementedError
