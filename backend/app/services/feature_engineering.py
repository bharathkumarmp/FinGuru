from datetime import datetime, timedelta

import numpy as np
from sqlalchemy.orm import Session

from app.models import (
    Customer,
    Transaction,
    Loan,
    EMIRecord,
    CustomerFeatures,
)


# ============================================================
# FEATURE ENGINEERING
# ============================================================

def calculate_customer_features(
    db: Session,
    customer_id: int,
):
    """
    Calculate financial features for a single customer.
    """

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise ValueError(
            f"Customer {customer_id} not found"
        )

    # --------------------------------------------------------
    # Fetch transactions
    # --------------------------------------------------------

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer_id
        )
        .all()
    )

    # --------------------------------------------------------
    # Fetch loans
    # --------------------------------------------------------

    loans = (
        db.query(Loan)
        .filter(
            Loan.customer_id == customer_id
        )
        .all()
    )

    # --------------------------------------------------------
    # Fetch EMI records
    # --------------------------------------------------------

    emi_records = (
        db.query(EMIRecord)
        .filter(
            EMIRecord.customer_id == customer_id
        )
        .all()
    )

    # --------------------------------------------------------
    # Basic transaction separation
    # --------------------------------------------------------

    income_transactions = [
        t for t in transactions
        if t.transaction_type.upper() == "CREDIT"
    ]

    spending_transactions = [
        t for t in transactions
        if t.transaction_type.upper() == "DEBIT"
    ]

    # --------------------------------------------------------
    # Income
    # --------------------------------------------------------

    total_income = sum(
        float(t.amount)
        for t in income_transactions
    )

    total_spending = sum(
        float(t.amount)
        for t in spending_transactions
    )

    # --------------------------------------------------------
    # Time range
    # --------------------------------------------------------

    dates = [
        t.timestamp
        for t in transactions
        if t.timestamp is not None
    ]

    if dates:

        min_date = min(dates)
        max_date = max(dates)

        days = max(
            (max_date - min_date).days,
            1,
        )

    else:

        days = 30

    months = max(
        days / 30,
        1,
    )

    # --------------------------------------------------------
    # Monthly income / spending
    # --------------------------------------------------------

    avg_monthly_income = (
        total_income / months
    )

    avg_monthly_spending = (
        total_spending / months
    )

    # --------------------------------------------------------
    # Savings rate
    # --------------------------------------------------------

    if avg_monthly_income > 0:

        savings_rate = (
            avg_monthly_income
            - avg_monthly_spending
        ) / avg_monthly_income

    else:

        savings_rate = 0.0

    savings_rate = float(
        np.clip(
            savings_rate,
            -1,
            1,
        )
    )

    # --------------------------------------------------------
    # EMI calculation
    # --------------------------------------------------------

    total_monthly_emi = sum(
        float(loan.monthly_emi or 0)
        for loan in loans
        if str(loan.status).upper()
        in ["ACTIVE", "ONGOING"]
    )

    if avg_monthly_income > 0:

        emi_ratio = (
            total_monthly_emi
            / avg_monthly_income
        )

    else:

        emi_ratio = 0.0

    emi_ratio = float(
        np.clip(
            emi_ratio,
            0,
            2,
        )
    )

    # --------------------------------------------------------
    # Missed EMI count
    # --------------------------------------------------------

    missed_emi_count = sum(
        1
        for emi in emi_records
        if str(emi.status).upper()
        in [
            "MISSED",
            "OVERDUE",
            "LATE",
        ]
    )

    # --------------------------------------------------------
    # Transaction frequency
    # --------------------------------------------------------

    transaction_frequency = (
        len(transactions) / months
    )

    # --------------------------------------------------------
    # Balance information
    # --------------------------------------------------------

    balances = []

    for t in sorted(
        transactions,
        key=lambda x: x.timestamp
        if x.timestamp
        else datetime.min,
    ):

        if t.transaction_type.upper() == "CREDIT":

            balances.append(
                float(t.amount)
            )

        else:

            balances.append(
                -float(t.amount)
            )

    if balances:

        cumulative_balance = np.cumsum(
            balances
        )

        average_balance = float(
            np.mean(cumulative_balance)
        )

        balance_std = float(
            np.std(cumulative_balance)
        )

        balance_volatility = (
            balance_std
            / max(
                abs(average_balance),
                1,
            )
        )

        cash_buffer = max(
            average_balance,
            0,
        )

    else:

        average_balance = 0.0
        balance_volatility = 0.0
        cash_buffer = 0.0

    # --------------------------------------------------------
    # Spending growth
    # --------------------------------------------------------

    spending_growth = 0.0

    if spending_transactions:

        sorted_spending = sorted(
            spending_transactions,
            key=lambda x: x.timestamp
            if x.timestamp
            else datetime.min,
        )

        midpoint = len(sorted_spending) // 2

        if midpoint > 0:

            first_half = sorted_spending[
                :midpoint
            ]

            second_half = sorted_spending[
                midpoint:
            ]

            first_avg = (
                sum(
                    float(t.amount)
                    for t in first_half
                )
                / len(first_half)
            )

            second_avg = (
                sum(
                    float(t.amount)
                    for t in second_half
                )
                / len(second_half)
            )

            if first_avg > 0:

                spending_growth = (
                    second_avg - first_avg
                ) / first_avg

    # --------------------------------------------------------
    # Income stability
    # --------------------------------------------------------

    income_amounts = [
        float(t.amount)
        for t in income_transactions
    ]

    if len(income_amounts) > 1:

        income_mean = np.mean(
            income_amounts
        )

        income_std = np.std(
            income_amounts
        )

        if income_mean > 0:

            income_stability = 1 - (
                income_std / income_mean
            )

        else:

            income_stability = 0.0

    else:

        income_stability = 0.5

    income_stability = float(
        np.clip(
            income_stability,
            0,
            1,
        )
    )

    # --------------------------------------------------------
    # Credit utilization
    # --------------------------------------------------------

    total_outstanding = sum(
        float(loan.outstanding_amount or 0)
        for loan in loans
        if str(loan.status).upper()
        in ["ACTIVE", "ONGOING"]
    )

    if avg_monthly_income > 0:

        credit_utilization = (
            total_outstanding
            / (avg_monthly_income * 12)
        )

    else:

        credit_utilization = 0.0

    credit_utilization = float(
        np.clip(
            credit_utilization,
            0,
            2,
        )
    )

    # --------------------------------------------------------
    # Save/update CustomerFeatures
    # --------------------------------------------------------

    features = (
        db.query(CustomerFeatures)
        .filter(
            CustomerFeatures.customer_id
            == customer_id
        )
        .first()
    )

    if features is None:

        features = CustomerFeatures(
            customer_id=customer_id
        )

        db.add(features)

    # --------------------------------------------------------
    # Assign calculated features
    # --------------------------------------------------------

    features.avg_monthly_income = (
        avg_monthly_income
    )

    features.avg_monthly_spending = (
        avg_monthly_spending
    )

    features.savings_rate = (
        savings_rate
    )

    features.emi_ratio = (
        emi_ratio
    )

    features.balance_volatility = (
        balance_volatility
    )

    features.spending_growth = (
        spending_growth
    )

    features.transaction_frequency = (
        transaction_frequency
    )

    features.credit_utilization = (
        credit_utilization
    )

    features.missed_emi_count = (
        missed_emi_count
    )

    features.income_stability = (
        income_stability
    )

    features.cash_buffer = (
        cash_buffer
    )

    db.commit()

    db.refresh(features)

    return features


# ============================================================
# CALCULATE ALL CUSTOMERS
# ============================================================

def calculate_all_customer_features(
    db: Session,
):
    """
    Calculate features for every customer.
    """

    customers = (
        db.query(Customer)
        .order_by(Customer.id)
        .all()
    )

    print(
        f"\nCalculating financial features "
        f"for {len(customers)} customers..."
    )

    results = []

    for customer in customers:

        try:

            features = (
                calculate_customer_features(
                    db,
                    customer.id,
                )
            )

            results.append(features)

            print(
                f"✓ Customer {customer.id}: "
                f"{customer.full_name}"
            )

        except Exception as exc:

            print(
                f"✗ Customer {customer.id} failed: "
                f"{exc}"
            )

    print(
        f"\n✓ Feature engineering complete: "
        f"{len(results)}/{len(customers)} customers"
    )

    return results