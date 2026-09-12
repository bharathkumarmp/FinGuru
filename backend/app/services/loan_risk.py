from math import pow

from sqlalchemy.orm import Session

from app.models import (
    Customer,
    CustomerFeatures,
    Loan,
)


# ============================================================
# EMI CALCULATOR
# ============================================================

def calculate_emi(
    principal: float,
    annual_interest_rate: float,
    tenure_months: int,
):
    """
    Calculate monthly loan EMI.
    """

    if principal <= 0:
        raise ValueError(
            "Loan amount must be greater than zero."
        )

    if tenure_months <= 0:
        raise ValueError(
            "Tenure must be greater than zero."
        )

    monthly_rate = (
        annual_interest_rate / 100 / 12
    )

    # Zero-interest case
    if monthly_rate == 0:
        return principal / tenure_months

    emi = (
        principal
        * monthly_rate
        * pow(
            1 + monthly_rate,
            tenure_months,
        )
        / (
            pow(
                1 + monthly_rate,
                tenure_months,
            )
            - 1
        )
    )

    return round(emi, 2)


# ============================================================
# LOAN RISK
# ============================================================

def calculate_loan_risk(
    features,
    loan_amount: float,
    tenure_months: int,
    interest_rate: float,
):
    """
    Evaluate whether a proposed loan is financially suitable.

    Returns a risk score from 0-100.
    Higher risk = less suitable.
    """

    income = float(
        features.avg_monthly_income or 0
    )

    current_spending = float(
        features.avg_monthly_spending or 0
    )

    current_emi_ratio = float(
        features.emi_ratio or 0
    )

    savings_rate = float(
        features.savings_rate or 0
    )

    missed_emi_count = int(
        features.missed_emi_count or 0
    )

    income_stability = float(
        features.income_stability or 0
    )

    cash_buffer = float(
        features.cash_buffer or 0
    )

    # --------------------------------------------------------
    # Proposed EMI
    # --------------------------------------------------------

    proposed_emi = calculate_emi(
        loan_amount,
        interest_rate,
        tenure_months,
    )

    # --------------------------------------------------------
    # Current EMI
    # --------------------------------------------------------

    if income > 0:

        current_emi = (
            current_emi_ratio * income
        )

    else:

        current_emi = 0

    # --------------------------------------------------------
    # New debt position
    # --------------------------------------------------------

    total_emi = (
        current_emi
        + proposed_emi
    )

    if income > 0:

        projected_emi_ratio = (
            total_emi / income
        )

        projected_surplus = (
            income
            - current_spending
            - proposed_emi
        )

    else:

        projected_emi_ratio = 1.0
        projected_surplus = -proposed_emi

    # ========================================================
    # RISK COMPONENTS
    # ========================================================

    risk_score = 0
    reasons = []

    # --------------------------------------------------------
    # 1. EMI burden — 30 points
    # --------------------------------------------------------

    if projected_emi_ratio <= 0.20:

        emi_risk = 0

    elif projected_emi_ratio <= 0.30:

        emi_risk = 8

    elif projected_emi_ratio <= 0.40:

        emi_risk = 18

    elif projected_emi_ratio <= 0.50:

        emi_risk = 25

    else:

        emi_risk = 30

        reasons.append(
            "Projected EMI burden is very high"
        )

    risk_score += emi_risk

    # --------------------------------------------------------
    # 2. Surplus — 25 points
    # --------------------------------------------------------

    if income <= 0:

        surplus_risk = 25

        reasons.append(
            "Insufficient income information"
        )

    else:

        surplus_ratio = (
            projected_surplus / income
        )

        if surplus_ratio >= 0.30:

            surplus_risk = 0

        elif surplus_ratio >= 0.20:

            surplus_risk = 8

        elif surplus_ratio >= 0.10:

            surplus_risk = 15

        elif surplus_ratio >= 0:

            surplus_risk = 20

        else:

            surplus_risk = 25

            reasons.append(
                "Loan would make monthly cash flow negative"
            )

    risk_score += surplus_risk

    # --------------------------------------------------------
    # 3. Savings — 15 points
    # --------------------------------------------------------

    if savings_rate >= 0.20:

        savings_risk = 0

    elif savings_rate >= 0.10:

        savings_risk = 5

    elif savings_rate >= 0:

        savings_risk = 10

    else:

        savings_risk = 15

        reasons.append(
            "Current savings position is weak"
        )

    risk_score += savings_risk

    # --------------------------------------------------------
    # 4. Income stability — 10 points
    # --------------------------------------------------------

    if income_stability >= 0.80:

        stability_risk = 0

    elif income_stability >= 0.60:

        stability_risk = 3

    elif income_stability >= 0.40:

        stability_risk = 6

    else:

        stability_risk = 10

        reasons.append(
            "Income shows significant variability"
        )

    risk_score += stability_risk

    # --------------------------------------------------------
    # 5. Existing missed EMIs — 10 points
    # --------------------------------------------------------

    if missed_emi_count == 0:

        payment_risk = 0

    elif missed_emi_count <= 2:

        payment_risk = 5

        reasons.append(
            "Previous missed EMI payments detected"
        )

    else:

        payment_risk = 10

        reasons.append(
            "Multiple missed EMI payments detected"
        )

    risk_score += payment_risk

    # --------------------------------------------------------
    # 6. Cash buffer — 10 points
    # --------------------------------------------------------

    if income > 0:

        buffer_months = (
            cash_buffer / income
        )

    else:

        buffer_months = 0

    if buffer_months >= 6:

        buffer_risk = 0

    elif buffer_months >= 3:

        buffer_risk = 3

    elif buffer_months >= 1:

        buffer_risk = 6

    else:

        buffer_risk = 10

        reasons.append(
            "Limited emergency cash buffer"
        )

    risk_score += buffer_risk

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    risk_score = max(
        0,
        min(
            100,
            round(risk_score),
        ),
    )

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if risk_score <= 20:

        risk_level = "LOW"

    elif risk_score <= 40:

        risk_level = "MODERATE"

    elif risk_score <= 60:

        risk_level = "HIGH"

    else:

        risk_level = "VERY_HIGH"

    # ========================================================
    # SUITABILITY
    # ========================================================

    if (
        projected_surplus < 0
        or projected_emi_ratio > 0.50
    ):

        suitability = "NOT_SUITABLE"

    elif (
        risk_score > 60
        or projected_emi_ratio > 0.40
    ):

        suitability = "HIGH_RISK"

    elif risk_score > 40:

        suitability = "CAUTION"

    else:

        suitability = "SUITABLE"

    # --------------------------------------------------------
    # Default reason
    # --------------------------------------------------------

    if not reasons:

        reasons.append(
            "Proposed loan appears manageable "
            "under current financial conditions"
        )

    return {
        "proposed_emi": proposed_emi,
        "current_emi": round(
            current_emi,
            2,
        ),
        "projected_emi_ratio": round(
            projected_emi_ratio,
            4,
        ),
        "projected_surplus": round(
            projected_surplus,
            2,
        ),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "suitability": suitability,
        "reasons": reasons,
    }


# ============================================================
# CUSTOMER LOAN ANALYSIS
# ============================================================

def evaluate_customer_loan(
    db: Session,
    customer_id: int,
    loan_amount: float,
    tenure_months: int,
    interest_rate: float,
):
    """
    Evaluate a proposed loan for a customer.
    """

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:

        raise ValueError(
            f"Customer {customer_id} not found"
        )

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
            f"Financial features not found "
            f"for customer {customer_id}"
        )

    result = calculate_loan_risk(
        features=features,
        loan_amount=loan_amount,
        tenure_months=tenure_months,
        interest_rate=interest_rate,
    )

    # --------------------------------------------------------
    # Existing loans
    # --------------------------------------------------------

    loans = (
        db.query(Loan)
        .filter(
            Loan.customer_id
            == customer_id
        )
        .all()
    )

    outstanding_amount = sum(
        float(
            loan.outstanding_amount or 0
        )
        for loan in loans
        if str(loan.status).upper()
        in [
            "ACTIVE",
            "ONGOING",
        ]
    )

    result["customer_id"] = customer_id

    result["loan_amount"] = loan_amount

    result["tenure_months"] = tenure_months

    result["interest_rate"] = interest_rate

    result[
        "existing_outstanding_amount"
    ] = round(
        outstanding_amount,
        2,
    )

    return result