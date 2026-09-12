from typing import Dict, Any


def check_bias(
    bias_score: float = 0.0,
    maximum_bias_score: float = 0.20,
) -> Dict[str, Any]:
    """
    Check whether the recommendation is within
    the permitted bias threshold.
    """

    if bias_score > maximum_bias_score:
        return {
            "passed": False,
            "bias_score": bias_score,
            "reason": (
                "Recommendation failed the configured "
                "bias threshold."
            ),
        }

    return {
        "passed": True,
        "bias_score": bias_score,
        "reason": (
            "Bias score is within the permitted threshold."
        ),
    }