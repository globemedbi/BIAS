"""
Claims Expert auditor — reconciles OCR data against authorization records.
"""
from enum import Enum
from typing import Any, Dict, List

from shared.communication_layer.logger import get_logger

logger = get_logger("CLAIMS_EXPERT")


class DiscrepancySeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AuditDecision(str, Enum):
    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    REJECTED = "REJECTED"


def determine_decision(
    within_policy: bool,
    discrepancies: List[Dict[str, Any]],
) -> AuditDecision:
    """
    Applies the decision logic from the SKILL.md spec.

    APPROVED: within_policy=true AND discrepancies=none or LOW only
    PENDING_REVIEW: within_policy=true AND discrepancies=MEDIUM
    REJECTED: within_policy=false OR discrepancies=HIGH
    """
    if not within_policy:
        return AuditDecision.REJECTED

    severities = {d.get("severity") for d in discrepancies}

    if DiscrepancySeverity.HIGH in severities:
        return AuditDecision.REJECTED
    if DiscrepancySeverity.MEDIUM in severities:
        return AuditDecision.PENDING_REVIEW
    return AuditDecision.APPROVED
