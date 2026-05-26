"""
Response formatter — adapts audit results to the user's role and tone.
"""
from typing import Any, Dict, List

from shared.communication_layer.logger import get_logger

logger = get_logger("CHATBOT")


def format_for_member(audit_result: Dict[str, Any]) -> str:
    """
    Formats for MEMBER users: plain language, no codes, focus on outcome.
    """
    decision = audit_result.get("decision", "UNKNOWN")
    messages = {
        "APPROVED": "Good news! Your claim has been approved.",
        "PENDING_REVIEW": "Your claim is under review. We'll update you soon.",
        "REJECTED": "Unfortunately, your claim could not be approved based on your coverage.",
    }
    return messages.get(decision, "Your claim is being processed.")


def format_for_adjuster(audit_result: Dict[str, Any]) -> str:
    """
    Formats for ADJUSTER users: technical detail, discrepancy codes, amounts.
    """
    decision = audit_result.get("decision", "UNKNOWN")
    discrepancies = audit_result.get("discrepancies", [])
    lines = [f"Decision: {decision}"]
    if discrepancies:
        lines.append("Discrepancies:")
        for d in discrepancies:
            lines.append(f"  - {d.get('field')}: {d.get('severity')} | OCR={d.get('ocr_value')} AUTH={d.get('auth_value')}")
    return "\n".join(lines)


def format_for_admin(audit_result: Dict[str, Any]) -> str:
    """
    Formats for ADMIN users: full detail including all metadata and audit trail.
    """
    import json
    return json.dumps(audit_result, indent=2, default=str)
