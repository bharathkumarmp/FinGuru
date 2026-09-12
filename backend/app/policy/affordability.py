from typing import Dict, Any


def check_affordability(
    affordability_score: float,
    projected_emi_ratio: float,
    monthly_surplus: float,
    maximum_emi_ratio: float = 0.50,
    minimum_affordability_score: float = 40.0,
) -> Dict[str, Any]:

    reasons = []

    if affordability_score < minimum_affordability_score:
        reasons.append(
            "Affordability score is below the permitted threshold."
        )

    if projected_emi_ratio > maximum_emi_ratio:
        reasons.append(
            "Projected EMI ratio exceeds the permitted threshold."
        )

    if monthly_surplus < 0:
        reasons.append(
            "Projected monthly cash flow is negative."
        )

    if reasons:
        return {
            "passed": False,
            "reasons": reasons,
            "affordability_score": affordability_score,
            "projected_emi_ratio": projected_emi_ratio,
            "monthly_surplus": monthly_surplus,
        }

    return {
        "passed": True,
        "reasons": [
            "Customer passes affordability checks."
        ],
        "affordability_score": affordability_score,
        "projected_emi_ratio": projected_emi_ratio,
        "monthly_surplus": monthly_surplus,
    }