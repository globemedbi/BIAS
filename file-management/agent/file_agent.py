"""
File Agent — orchestrates the OCR → Anonymize → Translate pipeline.
"""
from typing import Dict, List, Optional

from shared.communication_layer.logger import get_logger

logger = get_logger("FILE_MANAGEMENT")

PIPELINE_STEPS = ["download", "ocr", "anonymize", "translate", "validate", "upload"]


class FileAgent:
    """
    Executes the document processing pipeline.
    Pipeline order is STRICT — never reorder.
    Anonymization MUST complete before translation.
    OCR or anonymization failure STOPS the pipeline.
    Translation failure is a partial success — continue without translation.
    """

    async def process(
        self,
        file_uris: List[str],
        translate: bool = False,
        target_language: str = "en",
    ) -> Dict:
        """Runs the full pipeline for a list of file URIs."""
        raise NotImplementedError
