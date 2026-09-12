from typing import Dict, Any


def check_human_escalation(
    risk_score: float,
    confidence: float,
    critical: bool = False,
    minimum_confidence: float = 0.70,
) -> Dict[str, Any]:
    """
    Determine whether human review is required.
    """

    reasons = []

    if critical:
        reasons.append(
            "Critical risk requires human review."
        )

    if risk_score >= 75:
        reasons.append(
            "Risk score is critically high."
        )

    if confidence < minimum_confidence:
        reasons.append(
            "Low model confidence requires human review."
        )

    if reasons:
        return {
            "required": True,
            "reasons": reasons,
        }

    return {
        "required": False,
        "reasons": [],
    }