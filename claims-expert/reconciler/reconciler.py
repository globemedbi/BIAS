"""
Claims Expert reconciler — matches OCR data fields against authorization fields.
"""
from typing import Any, Dict, List

from shared.communication_layer.logger import get_logger

logger = get_logger("CLAIMS_EXPERT")


class Reconciler:
    """Compares OCR-extracted data against authorization records."""

    def reconcile(
        self,
        ocr_data: Dict[str, Any],
        auth_record: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Returns a list of discrepancies between OCR data and authorization.
        Each discrepancy has: field, ocr_value, auth_value, severity.
        """
        raise NotImplementedError
