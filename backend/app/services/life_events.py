from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models import Customer, Transaction


def detect_life_events(
    db: Session,
    customer_id: int,
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise ValueError(f"Customer {customer_id} not found")

    transactions = (
        db.query(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .order_by(Transaction.timestamp.asc())
        .all()
    )

    if not transactions:
        return {
            "customer_id": customer_id,
            "events": [],
        }

    events = []

    credits = [
        tx for tx in transactions
        if str(tx.transaction_type).upper() == "CREDIT"
    ]

    debits = [
        tx for tx in transactions
        if str(tx.transaction_type).upper() == "DEBIT"
    ]

    # ---------------------------------------------------------
    # 1. SALARY DETECTION
    # ---------------------------------------------------------

    salary_transactions = [
        tx for tx in credits
        if str(tx.category or "").lower() == "salary"
        or "salary" in str(tx.description or "").lower()
        or str(tx.merchant or "").lower() == "employer"
    ]

    if salary_transactions:
        latest_salary = salary_transactions[-1]

        events.append({
            "event_type": "SALARY_CREDITED",
            "confidence": 0.98,
            "timestamp": latest_salary.timestamp.isoformat(),
            "amount": float(latest_salary.amount),
            "description": "Regular salary income detected",
        })

    # ---------------------------------------------------------
    # 2. INCOME CHANGE
    # ---------------------------------------------------------

    monthly_income = defaultdict(float)

    for tx in salary_transactions:
        month = tx.timestamp.strftime("%Y-%m")
        monthly_income[month] += float(tx.amount or 0)

    income_values = list(monthly_income.values())

    if len(income_values) >= 2:
        previous_income = income_values[-2]
        current_income = income_values[-1]

        if previous_income > 0:
            change = (
                current_income - previous_income
            ) / previous_income

            if change <= -0.20:
                events.append({
                    "event_type": "INCOME_DECREASE",
                    "confidence": min(0.99, 0.70 + abs(change)),
                    "change_percent": round(change * 100, 2),
                    "description": "Significant salary income decrease detected",
                })

            elif change >= 0.20:
                events.append({
                    "event_type": "INCOME_INCREASE",
                    "confidence": min(0.99, 0.70 + change),
                    "change_percent": round(change * 100, 2),
                    "description": "Significant salary income increase detected",
                })

    # ---------------------------------------------------------
    # 3. SPENDING SPIKE
    # ---------------------------------------------------------

    monthly_spending = defaultdict(float)

    for tx in debits:
        month = tx.timestamp.strftime("%Y-%m")
        monthly_spending[month] += float(tx.amount or 0)

    spending_values = list(monthly_spending.values())

    if len(spending_values) >= 2:
        previous_spending = spending_values[-2]
        current_spending = spending_values[-1]

        if previous_spending > 0:
            spending_change = (
                current_spending - previous_spending
            ) / previous_spending

            if spending_change >= 0.30:
                events.append({
                    "event_type": "SPENDING_SPIKE",
                    "confidence": min(
                        0.99,
                        0.70 + spending_change,
                    ),
                    "change_percent": round(
                        spending_change * 100,
                        2,
                    ),
                    "description": "Monthly spending increased significantly",
                })

    # ---------------------------------------------------------
    # 4. LARGE TRANSACTION
    # ---------------------------------------------------------

    if transactions:
        debit_amounts = [
            float(tx.amount or 0)
            for tx in debits
            if float(tx.amount or 0) > 0
        ]

        if debit_amounts:
            average_transaction = (
                sum(debit_amounts) / len(debit_amounts)
            )

            for tx in debits:
                amount = float(tx.amount or 0)

                if (
                    amount >= average_transaction * 5
                    and amount >= 50000
                ):
                    events.append({
                        "event_type": "LARGE_PURCHASE",
                        "confidence": 0.90,
                        "timestamp": tx.timestamp.isoformat(),
                        "amount": amount,
                        "merchant": tx.merchant,
                        "category": tx.category,
                        "description": "Unusually large transaction detected",
                    })

    # ---------------------------------------------------------
    # 5. BALANCE DROP
    # ---------------------------------------------------------

    balance = 0.0
    balances = []

    for tx in transactions:
        if str(tx.transaction_type).upper() == "CREDIT":
            balance += float(tx.amount or 0)
        else:
            balance -= float(tx.amount or 0)

        balances.append({
            "timestamp": tx.timestamp,
            "balance": balance,
        })

    if len(balances) >= 2:
        previous_balance = balances[-2]["balance"]
        current_balance = balances[-1]["balance"]

        if (
            previous_balance > 0
            and current_balance < previous_balance * 0.50
        ):
            events.append({
                "event_type": "BALANCE_DROP",
                "confidence": 0.88,
                "previous_balance": round(
                    previous_balance,
                    2,
                ),
                "current_balance": round(
                    current_balance,
                    2,
                ),
                "description": "Significant account balance reduction detected",
            })

    # ---------------------------------------------------------
    # 6. NEW BENEFICIARIES
    # ---------------------------------------------------------

    seen_beneficiaries = set()

    for tx in transactions:
        beneficiary = tx.beneficiary

        if not beneficiary:
            continue

        if beneficiary not in seen_beneficiaries:
            seen_beneficiaries.add(beneficiary)

            events.append({
                "event_type": "NEW_BENEFICIARY",
                "confidence": 0.75,
                "beneficiary": beneficiary,
                "timestamp": tx.timestamp.isoformat(),
                "description": "New transaction beneficiary detected",
            })

    # ---------------------------------------------------------
    # SORT EVENTS
    # ---------------------------------------------------------

    events.sort(
        key=lambda event: event.get(
            "timestamp",
            "",
        ),
        reverse=True,
    )

    return {
        "customer_id": customer_id,
        "customer_name": customer.full_name,
        "event_count": len(events),
        "events": events,
    }


def detect_all_customer_events(
    db: Session,
):
    customers = db.query(Customer).all()

    results = []

    for customer in customers:
        try:
            result = detect_life_events(
                db,
                customer.id,
            )

            results.append(result)

        except Exception:
            db.rollback()

    return results
