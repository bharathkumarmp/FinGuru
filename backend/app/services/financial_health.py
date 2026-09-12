from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    CustomerFeatures,
    FinancialHealth,
)


# ============================================================
# FINANCIAL HEALTH ENGINE
# ============================================================


def calculate_health_components(features):
    """
    Calculate individual financial health components.

    Total score = 100 points.
    """

    # --------------------------------------------------------
    # Extract features safely
    # --------------------------------------------------------

    income = float(
        features.avg_monthly_income or 0
    )

    spending = float(
        features.avg_monthly_spending or 0
    )

    savings_rate = float(
        features.savings_rate or 0
    )

    emi_ratio = float(
        features.emi_ratio or 0
    )

    balance_volatility = float(
        features.balance_volatility or 0
    )

    income_stability = float(
        features.income_stability or 0
    )

    spending_growth = float(
        features.spending_growth or 0
    )

    credit_utilization = float(
        features.credit_utilization or 0
    )

    missed_emi_count = int(
        features.missed_emi_count or 0
    )

    cash_buffer = float(
        features.cash_buffer or 0
    )

    # ========================================================
    # 1. INCOME SCORE — 20
    # ========================================================

    if income <= 0:

        income_score = 0

    elif income_stability >= 0.80:

        income_score = 20

    elif income_stability >= 0.60:

        income_score = 16

    elif income_stability >= 0.40:

        income_score = 12

    else:

        income_score = 8

    # ========================================================
    # 2. SPENDING SCORE — 15
    # ========================================================

    if income <= 0:

        spending_score = 0

    else:

        spending_ratio = (
            spending / income
        )

        if spending_ratio <= 0.50:
            spending_score = 15

        elif spending_ratio <= 0.65:
            spending_score = 12

        elif spending_ratio <= 0.80:
            spending_score = 9

        elif spending_ratio <= 1.00:
            spending_score = 5

        else:
            spending_score = 0

    # ========================================================
    # 3. SAVINGS SCORE — 20
    # ========================================================

    if savings_rate >= 0.30:

        savings_score = 20

    elif savings_rate >= 0.20:

        savings_score = 17

    elif savings_rate >= 0.10:

        savings_score = 13

    elif savings_rate >= 0:

        savings_score = 8

    else:

        savings_score = 0

    # ========================================================
    # 4. DEBT SCORE — 20
    # ========================================================

    # EMI burden
    if emi_ratio <= 0.20:

        debt_score = 12

    elif emi_ratio <= 0.30:

        debt_score = 10

    elif emi_ratio <= 0.40:

        debt_score = 7

    elif emi_ratio <= 0.50:

        debt_score = 4

    else:

        debt_score = 1

    # Credit utilization component
    if credit_utilization <= 0.30:

        debt_score += 5

    elif credit_utilization <= 0.50:

        debt_score += 4

    elif credit_utilization <= 0.75:

        debt_score += 2

    else:

        debt_score += 0

    # Missed EMI penalty
    debt_score -= min(
        missed_emi_count * 2,
        5,
    )

    debt_score = max(
        0,
        min(
            20,
            debt_score,
        ),
    )

    # ========================================================
    # 5. STABILITY SCORE — 25
    # ========================================================

    # Income stability
    stability_score = (
        income_stability * 12
    )

    # Balance volatility
    if balance_volatility <= 0.10:

        stability_score += 8

    elif balance_volatility <= 0.25:

        stability_score += 6

    elif balance_volatility <= 0.50:

        stability_score += 4

    elif balance_volatility <= 1.00:

        stability_score += 2

    # Cash buffer
    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

    else:

        buffer_months = 0

    if buffer_months >= 6:

        stability_score += 5

    elif buffer_months >= 3:

        stability_score += 4

    elif buffer_months >= 1:

        stability_score += 2

    stability_score = max(
        0,
        min(
            25,
            round(stability_score),
        ),
    )

    # ========================================================
    # TOTAL SCORE
    # ========================================================

    score = (
        income_score
        + spending_score
        + savings_score
        + debt_score
        + stability_score
    )

    score = max(
        0,
        min(
            100,
            round(score),
        ),
    )

    return {
        "score": score,
        "income_score": round(
            income_score,
            2,
        ),
        "spending_score": round(
            spending_score,
            2,
        ),
        "savings_score": round(
            savings_score,
            2,
        ),
        "debt_score": round(
            debt_score,
            2,
        ),
        "stability_score": round(
            stability_score,
            2,
        ),
    }


# ============================================================
# HEALTH LEVEL
# ============================================================


def get_health_level(score):
    """
    Convert numerical score into a health level.
    """

    if score >= 80:

        return "EXCELLENT"

    elif score >= 65:

        return "GOOD"

    elif score >= 50:

        return "MODERATE"

    elif score >= 35:

        return "AT_RISK"

    else:

        return "CRITICAL"


# ============================================================
# EXPLANATIONS
# ============================================================


def generate_explanations(features, score):
    """
    Generate human-readable explanations.
    """

    strengths = []
    weaknesses = []
    recommendations = []

    income = float(
        features.avg_monthly_income or 0
    )

    spending = float(
        features.avg_monthly_spending or 0
    )

    savings_rate = float(
        features.savings_rate or 0
    )

    emi_ratio = float(
        features.emi_ratio or 0
    )

    income_stability = float(
        features.income_stability or 0
    )

    spending_growth = float(
        features.spending_growth or 0
    )

    missed_emi_count = int(
        features.missed_emi_count or 0
    )

    credit_utilization = float(
        features.credit_utilization or 0
    )

    cash_buffer = float(
        features.cash_buffer or 0
    )

    # --------------------------------------------------------
    # Strengths
    # --------------------------------------------------------

    if income_stability >= 0.70:

        strengths.append(
            "Stable income pattern"
        )

    if savings_rate >= 0.20:

        strengths.append(
            "Healthy savings rate"
        )

    if emi_ratio <= 0.30:

        strengths.append(
            "Manageable EMI burden"
        )

    if credit_utilization <= 0.50:

        strengths.append(
            "Healthy credit utilization"
        )

    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

        if buffer_months >= 3:

            strengths.append(
                "Strong cash buffer"
            )

    if missed_emi_count == 0:

        strengths.append(
            "No missed EMI payments"
        )

    # --------------------------------------------------------
    # Weaknesses
    # --------------------------------------------------------

    if spending > income:

        weaknesses.append(
            "Spending exceeds income"
        )

    elif income > 0:

        spending_ratio = (
            spending / income
        )

        if spending_ratio > 0.80:

            weaknesses.append(
                "High spending relative to income"
            )

    if savings_rate < 0.10:

        weaknesses.append(
            "Low savings rate"
        )

    if emi_ratio > 0.40:

        weaknesses.append(
            "High EMI burden"
        )

    if spending_growth > 0.20:

        weaknesses.append(
            "Spending is increasing rapidly"
        )

    if credit_utilization > 0.75:

        weaknesses.append(
            "High credit utilization"
        )

    if missed_emi_count > 0:

        weaknesses.append(
            f"{missed_emi_count} missed EMI payment(s)"
        )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    if savings_rate < 0.10:

        recommendations.append(
            "Increase monthly savings"
        )

    if emi_ratio > 0.40:

        recommendations.append(
            "Avoid taking on additional debt"
        )

    if spending_growth > 0.20:

        recommendations.append(
            "Review recent spending increases"
        )

    if credit_utilization > 0.75:

        recommendations.append(
            "Reduce outstanding credit utilization"
        )

    if missed_emi_count > 0:

        recommendations.append(
            "Prioritize timely EMI payments"
        )

    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

        if buffer_months < 3:

            recommendations.append(
                "Build an emergency cash buffer"
            )

    if not recommendations:

        recommendations.append(
            "Maintain current financial habits"
        )

    # --------------------------------------------------------
    # Fallback explanations
    # --------------------------------------------------------

    if not strengths:

        strengths.append(
            "Financial profile is being monitored"
        )

    if not weaknesses:

        weaknesses.append(
            "No major financial weakness detected"
        )

    return {
        "strengths": "; ".join(
            strengths
        ),

        "weaknesses": "; ".join(
            weaknesses
        ),

        "recommendations": "; ".join(
            recommendations
        ),
    }


# ============================================================
# CALCULATE ONE CUSTOMER
# ============================================================


def calculate_customer_health(
    db: Session,
    customer_id: int,
):
    """
    Calculate and store financial health
    for one customer.
    """

    features = (
        db.query(CustomerFeatures)
        .filter(
            CustomerFeatures.customer_id
            == customer_id
        )
        .first()
    )

    if not features:

        raise ValueError(
            f"No CustomerFeatures found "
            f"for customer {customer_id}"
        )

    # --------------------------------------------------------
    # Calculate score
    # --------------------------------------------------------

    components = calculate_health_components(
        features
    )

    score = components["score"]

    health_level = get_health_level(
        score
    )

    # --------------------------------------------------------
    # Generate explanations
    # --------------------------------------------------------

    explanations = generate_explanations(
        features,
        score,
    )

    # --------------------------------------------------------
    # Find existing health record
    # --------------------------------------------------------

    health = (
        db.query(FinancialHealth)
        .filter(
            FinancialHealth.customer_id
            == customer_id
        )
        .first()
    )

    if health is None:

        health = FinancialHealth(
            customer_id=customer_id
        )

        db.add(health)

    # --------------------------------------------------------
    # Store values using YOUR model's fields
    # --------------------------------------------------------

    health.score = score

    health.health_level = (
        health_level
    )

    health.income_score = (
        components["income_score"]
    )

    health.spending_score = (
        components["spending_score"]
    )

    health.savings_score = (
        components["savings_score"]
    )

    health.debt_score = (
        components["debt_score"]
    )

    health.stability_score = (
        components["stability_score"]
    )

    health.monthly_income = (
        features.avg_monthly_income or 0
    )

    health.monthly_spending = (
        features.avg_monthly_spending or 0
    )

    health.savings_rate = (
        features.savings_rate or 0
    )

    health.emi_ratio = (
        features.emi_ratio or 0
    )

    health.balance_volatility = (
        features.balance_volatility or 0
    )

    health.strengths = (
        explanations["strengths"]
    )

    health.weaknesses = (
        explanations["weaknesses"]
    )

    health.recommendations = (
        explanations["recommendations"]
    )

    health.calculated_at = datetime.utcnow()

    db.commit()

    db.refresh(health)

    return health


# ============================================================
# CALCULATE ALL CUSTOMERS
# ============================================================


def calculate_all_health_scores(
    db: Session,
):
    """
    Calculate financial health for all
    customers with feature records.
    """

    features_list = (
        db.query(CustomerFeatures)
        .order_by(
            CustomerFeatures.customer_id
        )
        .all()
    )

    print(
        f"\nCalculating financial health "
        f"for {len(features_list)} customers..."
    )

    results = []

    for features in features_list:

        customer_id = (
            features.customer_id
        )

        try:

            health = (
                calculate_customer_health(
                    db,
                    customer_id,
                )
            )

            results.append(health)

            print(
                f"✓ Customer {customer_id}: "
                f"{health.score}/100 "
                f"({health.health_level})"
            )

        except Exception as exc:

            # Roll back this customer's
            # failed transaction so the
            # session remains usable.

            db.rollback()

            print(
                f"✗ Customer {customer_id} failed: "
                f"{exc}"
            )

    print(
        f"\n✓ Financial health calculation "
        f"complete: "
        f"{len(results)}/{len(features_list)}"
    )

    return results