from typing import Dict, Any


def check_confidence(
    confidence: float,
    minimum_confidence: float = 0.70,
) -> Dict[str, Any]:
    """
    Check whether model confidence is sufficient
    for an automated recommendation.
    """

    if confidence < minimum_confidence:
        return {
            "passed": False,
            "confidence": confidence,
            "reason": (
                "Model confidence is below the "
                "required threshold."
            ),
        }

    return {
        "passed": True,
        "confidence": confidence,
        "reason": (
            "Model confidence is sufficient."
        ),
    }