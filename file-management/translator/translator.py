"""
Translator client — translates anonymized text to a target language.
Only receives pre-anonymized text. Never receives raw PII.
"""
from typing import Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("FILE_MANAGEMENT")


class Translator:
    """Translates anonymized text. Only call after Anonymizer has run."""

    async def translate(self, text: str, target_language: str) -> Optional[str]:
        """
        Translates text to the target language.
        Returns translated text, or None on failure (pipeline continues without translation).
        """
        raise NotImplementedError
