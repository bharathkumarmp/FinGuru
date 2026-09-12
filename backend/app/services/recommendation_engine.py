from typing import Dict, Any


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(maximum, value))


def calculate_need_score(
    health_score: float,
    stress_score: float,
    loan_required: bool = False,
) -> float:
    """
    Estimate how strongly the customer needs intervention.
    Higher score = greater need for action.
    """

    health_pressure = 100 - health_score
    stress_pressure = stress_score

    score = (
        health_pressure * 0.45
        + stress_pressure * 0.45
        + (10 if loan_required else 0)
    )

    return round(clamp(score), 2)


def calculate_affordability_score(
    monthly_income: float,
    monthly_surplus: float,
    projected_emi_ratio: float = 0,
) -> float:
    """
    Estimate affordability using surplus and EMI burden.
    """

    if monthly_income <= 0:
        return 0

    surplus_ratio = monthly_surplus / monthly_income

    surplus_score = clamp((surplus_ratio + 0.25) * 100)

    emi_score = clamp(100 - projected_emi_ratio * 100)

    score = (
        surplus_score * 0.6
        + emi_score * 0.4
    )

    return round(clamp(score), 2)


def calculate_suitability_score(
    health_score: float,
    stress_score: float,
    loan_suitable: bool = True,
) -> float:
    """
    Estimate whether the proposed financial action is suitable.
    """

    if not loan_suitable:
        return 0

    score = (
        health_score * 0.5
        + (100 - stress_score) * 0.5
    )

    return round(clamp(score), 2)


def calculate_timing_score(
    health_score: float,
    stress_score: float,
) -> float:
    """
    Determines whether this is a good time to act.
    """

    score = (
        health_score * 0.5
        + (100 - stress_score) * 0.5
    )

    return round(clamp(score), 2)


def calculate_recommendation_score(
    need_score: float,
    affordability_score: float,
    suitability_score: float,
    timing_score: float,
    customer_preference: float = 50,
    financial_health: float = 50,
) -> float:
    """
    Prescriptive recommendation score.

    ML/statistical engines provide the inputs.
    This layer evaluates those signals.
    """

    score = (
        need_score * 0.20
        + affordability_score * 0.20
        + suitability_score * 0.20
        + timing_score * 0.15
        + customer_preference * 0.10
        + financial_health * 0.15
    )

    return round(clamp(score), 2)


def generate_recommendation(
    health_score: float,
    stress_score: float,
    monthly_income: float,
    monthly_surplus: float,
    projected_emi_ratio: float = 0,
    loan_suitable: bool = True,
    fraud_risk: float = 0,
    customer_preference: float = 50,
    loan_requested: bool = False,
) -> Dict[str, Any]:

    # ---------------------------------------------------------
    # 1. Calculate prescriptive signals
    # ---------------------------------------------------------

    need_score = calculate_need_score(
        health_score=health_score,
        stress_score=stress_score,
        loan_required=loan_requested,
    )

    affordability_score = calculate_affordability_score(
        monthly_income=monthly_income,
        monthly_surplus=monthly_surplus,
        projected_emi_ratio=projected_emi_ratio,
    )

    suitability_score = calculate_suitability_score(
        health_score=health_score,
        stress_score=stress_score,
        loan_suitable=loan_suitable,
    )

    timing_score = calculate_timing_score(
        health_score=health_score,
        stress_score=stress_score,
    )

    recommendation_score = calculate_recommendation_score(
        need_score=need_score,
        affordability_score=affordability_score,
        suitability_score=suitability_score,
        timing_score=timing_score,
        customer_preference=customer_preference,
        financial_health=health_score,
    )

    # ---------------------------------------------------------
    # 2. Policy / safety guardrails
    # ---------------------------------------------------------

    reasons = []
    recommendation = "NO_ACTION"

    # CRITICAL SECURITY GUARDRAIL
    if fraud_risk >= 75:
        recommendation = "WARN"
        reasons.append("Critical fraud or account-security risk detected.")

    elif fraud_risk >= 50:
        recommendation = "WARN"
        reasons.append("High transaction or account-security risk detected.")

    # CRITICAL FINANCIAL STRESS
    elif stress_score >= 80:
        recommendation = "SEEK_HELP"
        reasons.append(
            "Financial stress is critically high and requires intervention."
        )

    # LOAN UNSUITABLE
    elif loan_requested and not loan_suitable:
        recommendation = "WAIT"
        reasons.append(
            "The proposed financial product is not currently suitable."
        )

    # UNAFFORDABLE LOAN
    elif loan_requested and (
        monthly_surplus < 0
        or projected_emi_ratio > 0.50
    ):
        recommendation = "WAIT"
        reasons.append(
            "The proposed loan creates an excessive financial burden."
        )

    # HIGH STRESS
    elif stress_score >= 60:
        recommendation = "WAIT"
        reasons.append(
            "Financial stress is high; taking additional financial obligations "
            "should be delayed."
        )

    # LOW HEALTH
    elif health_score < 35:
        recommendation = "SEEK_HELP"
        reasons.append(
            "Financial health is critically low."
        )

    elif health_score < 50:
        recommendation = "WAIT"
        reasons.append(
            "Financial health needs improvement before taking additional obligations."
        )

    # LOW SAVINGS / LOW AFFORDABILITY
    elif affordability_score < 40:
        recommendation = "SAVE"
        reasons.append(
            "Increasing savings and financial buffer should be prioritized."
        )

    # GOOD FINANCIAL POSITION
    elif (
        recommendation_score >= 70
        and health_score >= 65
        and stress_score < 40
    ):
        recommendation = "APPLY"
        reasons.append(
            "Financial health, affordability and timing are favorable."
        )

    else:
        recommendation = "NO_ACTION"
        reasons.append(
            "No immediate financial intervention is required."
        )

    # ---------------------------------------------------------
    # 3. Additional explanations
    # ---------------------------------------------------------

    if monthly_surplus < 0:
        reasons.append(
            "Current monthly cash flow is negative."
        )

    if projected_emi_ratio > 0.40:
        reasons.append(
            "EMI burden would become significant relative to income."
        )

    if stress_score >= 60:
        reasons.append(
            "Current financial stress is elevated."
        )

    if health_score < 50:
        reasons.append(
            "Financial health score is below the preferred range."
        )

    return {
        "recommendation": recommendation,
        "recommendation_score": recommendation_score,
        "signals": {
            "need_score": need_score,
            "affordability_score": affordability_score,
            "suitability_score": suitability_score,
            "timing_score": timing_score,
            "customer_preference": customer_preference,
            "financial_health": health_score,
        },
        "guardrails": {
            "fraud_risk": fraud_risk,
            "stress_score": stress_score,
            "loan_suitable": loan_suitable,
        },
        "reasons": reasons,
    }