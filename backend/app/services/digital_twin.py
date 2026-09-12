from sqlalchemy.orm import Session

from app.models import CustomerFeatures, FinancialHealth, FinancialStress
from app.services.loan_risk import calculate_emi


def calculate_projected_health(
    current_health_score: float,
    projected_emi_ratio: float,
    projected_surplus: float,
    income: float,
    current_savings_rate: float,
):
    score = float(current_health_score)

    # EMI burden impact
    if projected_emi_ratio > 0.50:
        score -= 18
    elif projected_emi_ratio > 0.40:
        score -= 12
    elif projected_emi_ratio > 0.30:
        score -= 7
    elif projected_emi_ratio > 0.20:
        score -= 3

    # Cash-flow impact
    if projected_surplus < 0:
        score -= 20
    elif income > 0:
        surplus_ratio = projected_surplus / income

        if surplus_ratio < 0.10:
            score -= 10
        elif surplus_ratio < 0.20:
            score -= 5

    # Savings capacity
    if current_savings_rate < 0.10:
        score -= 4

    return max(0, min(100, round(score)))


def calculate_projected_stress(
    current_stress_score: float,
    projected_emi_ratio: float,
    projected_surplus: float,
    income: float,
):
    score = float(current_stress_score)

    if projected_emi_ratio > 0.50:
        score += 25
    elif projected_emi_ratio > 0.40:
        score += 18
    elif projected_emi_ratio > 0.30:
        score += 10
    elif projected_emi_ratio > 0.20:
        score += 5

    if projected_surplus < 0:
        score += 20
    elif income > 0:
        surplus_ratio = projected_surplus / income

        if surplus_ratio < 0.10:
            score += 12
        elif surplus_ratio < 0.20:
            score += 6

    return max(0, min(100, round(score)))


def get_stress_level(score: float):
    if score <= 20:
        return "LOW"
    elif score <= 40:
        return "MODERATE"
    elif score <= 60:
        return "HIGH"
    elif score <= 80:
        return "VERY_HIGH"
    return "CRITICAL"


def simulate_financial_future(
    db: Session,
    customer_id: int,
    loan_amount: float,
    tenure_months: int,
    interest_rate: float,
):
    features = (
        db.query(CustomerFeatures)
        .filter(CustomerFeatures.customer_id == customer_id)
        .first()
    )

    if not features:
        raise ValueError(
            f"Financial features not found for customer {customer_id}"
        )

    health = (
        db.query(FinancialHealth)
        .filter(FinancialHealth.customer_id == customer_id)
        .order_by(FinancialHealth.calculated_at.desc())
        .first()
    )

    stress = (
        db.query(FinancialStress)
        .filter(FinancialStress.customer_id == customer_id)
        .order_by(FinancialStress.calculated_at.desc())
        .first()
    )

    if not health:
        raise ValueError(
            f"Financial health not found for customer {customer_id}"
        )

    if not stress:
        raise ValueError(
            f"Financial stress not found for customer {customer_id}"
        )

    income = float(features.avg_monthly_income or 0)
    spending = float(features.avg_monthly_spending or 0)
    savings_rate = float(features.savings_rate or 0)
    cash_buffer = float(features.cash_buffer or 0)

    current_health = float(health.score or 0)

    current_stress = float(
        getattr(
            stress,
            "stress_score",
            getattr(stress, "score", 0),
        )
        or 0
    )

    current_emi_ratio = float(features.emi_ratio or 0)

    current_emi = current_emi_ratio * income

    new_emi = calculate_emi(
        loan_amount,
        interest_rate,
        tenure_months,
    )

    current_surplus = income - spending - current_emi

    projected_total_emi = current_emi + new_emi

    if income > 0:
        projected_emi_ratio = projected_total_emi / income
    else:
        projected_emi_ratio = 1.0

    projected_surplus = (
        income
        - spending
        - projected_total_emi
    )

    # Estimate remaining cash buffer after taking the loan.
    projected_cash_buffer = max(
        0,
        cash_buffer - max(0, new_emi * 3),
    )

    projected_health = calculate_projected_health(
        current_health_score=current_health,
        projected_emi_ratio=projected_emi_ratio,
        projected_surplus=projected_surplus,
        income=income,
        current_savings_rate=savings_rate,
    )

    projected_stress = calculate_projected_stress(
        current_stress_score=current_stress,
        projected_emi_ratio=projected_emi_ratio,
        projected_surplus=projected_surplus,
        income=income,
    )

    stress_level = get_stress_level(
        projected_stress
    )

    # ---------------------------------------------------------
    # NEXT BEST ACTION
    # ---------------------------------------------------------

    reasons = []

    if projected_surplus < 0:
        recommendation = "WAIT"
        reasons.append(
            "The proposed loan would make monthly cash flow negative"
        )

    elif projected_emi_ratio > 0.50:
        recommendation = "WAIT"
        reasons.append(
            "Total EMI burden would become very high"
        )

    elif projected_stress >= 60:
        recommendation = "WAIT"
        reasons.append(
            "Projected financial stress becomes high"
        )

    elif projected_health < current_health - 10:
        recommendation = "WAIT"
        reasons.append(
            "Financial health would decline significantly"
        )

    elif projected_health >= current_health and projected_stress < 40:
        recommendation = "APPLY"
        reasons.append(
            "The proposed loan appears manageable under the simulated conditions"
        )

    else:
        recommendation = "WAIT"
        reasons.append(
            "The simulated loan requires caution"
        )

    if projected_emi_ratio > current_emi_ratio:
        reasons.append(
            "EMI burden increases after the proposed loan"
        )

    if projected_cash_buffer < cash_buffer:
        reasons.append(
            "Emergency cash buffer decreases"
        )

    return {
        "customer_id": customer_id,

        "current_state": {
            "monthly_income": round(income, 2),
            "monthly_spending": round(spending, 2),
            "existing_emi": round(current_emi, 2),
            "monthly_surplus": round(current_surplus, 2),
            "cash_buffer": round(cash_buffer, 2),
            "health_score": round(current_health),
            "stress_score": round(current_stress),
        },

        "simulation": {
            "loan_amount": round(loan_amount, 2),
            "tenure_months": tenure_months,
            "interest_rate": interest_rate,
            "new_emi": round(new_emi, 2),
        },

        "projected_state": {
            "total_emi": round(projected_total_emi, 2),
            "emi_ratio": round(projected_emi_ratio, 4),
            "monthly_surplus": round(
                projected_surplus,
                2,
            ),
            "cash_buffer": round(
                projected_cash_buffer,
                2,
            ),
            "health_score": projected_health,
            "stress_score": projected_stress,
            "stress_level": stress_level,
        },

        "impact": {
            "health_change": round(
                projected_health - current_health
            ),
            "stress_change": round(
                projected_stress - current_stress
            ),
            "surplus_change": round(
                projected_surplus - current_surplus,
                2,
            ),
            "cash_buffer_change": round(
                projected_cash_buffer - cash_buffer,
                2,
            ),
        },

        "recommendation": recommendation,
        "reasons": reasons,
    }
