from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    CustomerFeatures,
    FinancialStress,
)


# ============================================================
# FINANCIAL STRESS ENGINE
# ============================================================


def calculate_stress_score(features):
    """
    Calculate financial stress on a 0-100 scale.

    0   = very low stress
    100 = very high stress
    """

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

    spending_growth = float(
        features.spending_growth or 0
    )

    missed_emi_count = int(
        features.missed_emi_count or 0
    )

    credit_utilization = float(
        features.credit_utilization or 0
    )

    income_stability = float(
        features.income_stability or 0
    )

    cash_buffer = float(
        features.cash_buffer or 0
    )

    # ========================================================
    # 1. SPENDING PRESSURE — 25 points
    # ========================================================

    if income > 0:

        spending_ratio = (
            spending / income
        )

    else:

        spending_ratio = 1.5

    if spending_ratio <= 0.50:

        spending_pressure = 0

    elif spending_ratio <= 0.65:

        spending_pressure = 8

    elif spending_ratio <= 0.80:

        spending_pressure = 15

    elif spending_ratio <= 1.00:

        spending_pressure = 20

    else:

        spending_pressure = 25

    # ========================================================
    # 2. DEBT PRESSURE — 25 points
    # ========================================================

    if emi_ratio <= 0.20:

        debt_pressure = 2

    elif emi_ratio <= 0.30:

        debt_pressure = 8

    elif emi_ratio <= 0.40:

        debt_pressure = 14

    elif emi_ratio <= 0.50:

        debt_pressure = 20

    else:

        debt_pressure = 25

    # ========================================================
    # 3. SAVINGS PRESSURE — 15 points
    # ========================================================

    if savings_rate >= 0.30:

        savings_pressure = 0

    elif savings_rate >= 0.20:

        savings_pressure = 3

    elif savings_rate >= 0.10:

        savings_pressure = 7

    elif savings_rate >= 0:

        savings_pressure = 11

    else:

        savings_pressure = 15

    # ========================================================
    # 4. INCOME INSTABILITY — 10 points
    # ========================================================

    income_instability = (
        1 - income_stability
    )

    income_instability = max(
        0,
        min(
            1,
            income_instability,
        ),
    )

    income_stress = (
        income_instability * 10
    )

    # ========================================================
    # 5. SPENDING GROWTH — 10 points
    # ========================================================

    if spending_growth <= 0:

        growth_stress = 0

    elif spending_growth <= 0.10:

        growth_stress = 3

    elif spending_growth <= 0.20:

        growth_stress = 6

    elif spending_growth <= 0.40:

        growth_stress = 8

    else:

        growth_stress = 10

    # ========================================================
    # 6. CASH BUFFER — 10 points
    # ========================================================

    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

    else:

        buffer_months = 0

    if buffer_months >= 6:

        buffer_stress = 0

    elif buffer_months >= 3:

        buffer_stress = 3

    elif buffer_months >= 1:

        buffer_stress = 6

    elif buffer_months > 0:

        buffer_stress = 8

    else:

        buffer_stress = 10

    # ========================================================
    # 7. BEHAVIORAL / PAYMENT PRESSURE — 5 points
    # ========================================================

    behavioral_stress = 0

    if missed_emi_count > 0:

        behavioral_stress += min(
            missed_emi_count * 2,
            4,
        )

    if credit_utilization > 0.75:

        behavioral_stress += 1

    behavioral_stress = min(
        behavioral_stress,
        5,
    )

    # ========================================================
    # TOTAL
    # ========================================================

    stress_score = (
        spending_pressure
        + debt_pressure
        + savings_pressure
        + income_stress
        + growth_stress
        + buffer_stress
        + behavioral_stress
    )

    # Small contribution from balance volatility
    if balance_volatility > 0.50:

        stress_score += 3

    elif balance_volatility > 0.25:

        stress_score += 1

    stress_score = max(
        0,
        min(
            100,
            round(stress_score),
        ),
    )

    # ========================================================
    # STRESS LEVEL
    # ========================================================

    if stress_score <= 20:

        stress_level = "LOW"

    elif stress_score <= 40:

        stress_level = "MODERATE"

    elif stress_score <= 60:

        stress_level = "HIGH"

    elif stress_score <= 80:

        stress_level = "VERY_HIGH"

    else:

        stress_level = "CRITICAL"

    return (
        stress_score,
        stress_level,
    )


# ============================================================
# STRESS FACTORS
# ============================================================


def generate_stress_factors(features):
    """
    Generate explainable stress factors.
    """

    factors = []

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

    spending_growth = float(
        features.spending_growth or 0
    )

    missed_emi_count = int(
        features.missed_emi_count or 0
    )

    credit_utilization = float(
        features.credit_utilization or 0
    )

    income_stability = float(
        features.income_stability or 0
    )

    cash_buffer = float(
        features.cash_buffer or 0
    )

    # --------------------------------------------------------
    # Spending
    # --------------------------------------------------------

    if income > 0:

        spending_ratio = (
            spending / income
        )

        if spending_ratio > 1:

            factors.append(
                "Spending exceeds income"
            )

        elif spending_ratio > 0.80:

            factors.append(
                "High spending relative to income"
            )

    # --------------------------------------------------------
    # Savings
    # --------------------------------------------------------

    if savings_rate < 0.10:

        factors.append(
            "Low savings rate"
        )

    # --------------------------------------------------------
    # Debt
    # --------------------------------------------------------

    if emi_ratio > 0.50:

        factors.append(
            "Very high EMI burden"
        )

    elif emi_ratio > 0.40:

        factors.append(
            "High EMI burden"
        )

    # --------------------------------------------------------
    # Spending growth
    # --------------------------------------------------------

    if spending_growth > 0.20:

        factors.append(
            "Rapid spending growth"
        )

    # --------------------------------------------------------
    # Income
    # --------------------------------------------------------

    if income_stability < 0.50:

        factors.append(
            "Income instability"
        )

    # --------------------------------------------------------
    # Cash buffer
    # --------------------------------------------------------

    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

        if buffer_months < 1:

            factors.append(
                "Very limited cash buffer"
            )

        elif buffer_months < 3:

            factors.append(
                "Limited emergency buffer"
            )

    # --------------------------------------------------------
    # EMI
    # --------------------------------------------------------

    if missed_emi_count > 0:

        factors.append(
            f"{missed_emi_count} missed EMI payment(s)"
        )

    # --------------------------------------------------------
    # Credit
    # --------------------------------------------------------

    if credit_utilization > 0.75:

        factors.append(
            "High credit utilization"
        )

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    if not factors:

        factors.append(
            "No major financial stress indicator detected"
        )

    return factors


# ============================================================
# SAVE ONE CUSTOMER
# ============================================================


def calculate_customer_stress(
    db: Session,
    customer_id: int,
):
    """
    Calculate and store stress for one customer.
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
            f"No features found for customer "
            f"{customer_id}"
        )

    stress_score, stress_level = (
        calculate_stress_score(
            features
        )
    )

    factors = generate_stress_factors(
        features
    )

    # --------------------------------------------------------
    # Existing record?
    # --------------------------------------------------------

    stress = (
        db.query(FinancialStress)
        .filter(
            FinancialStress.customer_id
            == customer_id
        )
        .first()
    )

    if stress is None:

        stress = FinancialStress(
            customer_id=customer_id
        )

        db.add(stress)

    # --------------------------------------------------------
    # Store using common FinancialStress fields
    # --------------------------------------------------------

    if hasattr(stress, "stress_score"):

        stress.stress_score = stress_score

    elif hasattr(stress, "score"):

        stress.score = stress_score

    if hasattr(stress, "stress_level"):

        stress.stress_level = stress_level

    elif hasattr(stress, "level"):

        stress.level = stress_level

    if hasattr(stress, "stress_factors"):

        stress.stress_factors = "; ".join(
            factors
        )

    elif hasattr(stress, "factors"):

        stress.factors = "; ".join(
            factors
        )

    if hasattr(stress, "calculated_at"):

        stress.calculated_at = (
            datetime.utcnow()
        )

    db.commit()

    db.refresh(stress)

    return stress


# ============================================================
# ALL CUSTOMERS
# ============================================================


def calculate_all_stress_scores(
    db: Session,
):
    """
    Calculate stress for all customers.
    """

    features_list = (
        db.query(CustomerFeatures)
        .order_by(
            CustomerFeatures.customer_id
        )
        .all()
    )

    print(
        f"\nCalculating financial stress "
        f"for {len(features_list)} customers..."
    )

    results = []

    for features in features_list:

        customer_id = (
            features.customer_id
        )

        try:

            stress = (
                calculate_customer_stress(
                    db,
                    customer_id,
                )
            )

            results.append(stress)

            # Read whichever score field exists
            score = getattr(
                stress,
                "stress_score",
                getattr(
                    stress,
                    "score",
                    None,
                ),
            )

            level = getattr(
                stress,
                "stress_level",
                getattr(
                    stress,
                    "level",
                    "UNKNOWN",
                ),
            )

            print(
                f"✓ Customer {customer_id}: "
                f"{score}/100 ({level})"
            )

        except Exception as exc:

            db.rollback()

            print(
                f"✗ Customer {customer_id} failed: "
                f"{exc}"
            )

    print(
        f"\n✓ Financial stress calculation "
        f"complete: "
        f"{len(results)}/{len(features_list)}"
    )

    return results