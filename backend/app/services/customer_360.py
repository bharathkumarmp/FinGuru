from sqlalchemy.orm import Session

from app.models import (
    Customer,
    Account,
    Transaction,
    Loan,
    EMIRecord,
    CustomerFeatures,
    FinancialHealth,
    FinancialStress,
)


def get_customer_360(db: Session, customer_id: int):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise ValueError(f"Customer {customer_id} not found")

    accounts = (
        db.query(Account)
        .filter(Account.customer_id == customer_id)
        .all()
    )

    transactions = (
        db.query(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    loans = (
        db.query(Loan)
        .filter(Loan.customer_id == customer_id)
        .all()
    )

    emi_records = (
        db.query(EMIRecord)
        .filter(EMIRecord.customer_id == customer_id)
        .all()
    )

    features = (
        db.query(CustomerFeatures)
        .filter(CustomerFeatures.customer_id == customer_id)
        .first()
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

    total_balance = sum(
        float(account.balance or 0)
        for account in accounts
    )

    total_credit = sum(
        float(tx.amount or 0)
        for tx in transactions
        if str(tx.transaction_type).upper() == "CREDIT"
    )

    total_debit = sum(
        float(tx.amount or 0)
        for tx in transactions
        if str(tx.transaction_type).upper() == "DEBIT"
    )

    active_loans = [
        loan
        for loan in loans
        if str(loan.status).upper() in ["ACTIVE", "ONGOING"]
    ]

    outstanding_loans = sum(
        float(loan.outstanding_amount or 0)
        for loan in active_loans
    )

    return {
        "customer": {
            "id": customer.id,
            "customer_code": customer.customer_code,
            "full_name": customer.full_name,
            "email": customer.email,
            "phone": customer.phone,
            "city": customer.city,
            "occupation": customer.occupation,
            "monthly_income": float(customer.monthly_income or 0),
        },

        "accounts": {
            "count": len(accounts),
            "total_balance": round(total_balance, 2),
        },

        "transactions": {
            "count": len(transactions),
            "total_credit": round(total_credit, 2),
            "total_debit": round(total_debit, 2),
        },

        "loans": {
            "total": len(loans),
            "active": len(active_loans),
            "outstanding_amount": round(outstanding_loans, 2),
        },

        "emi": {
            "total_records": len(emi_records),
            "missed_count": sum(
                1
                for emi in emi_records
                if str(getattr(emi, "status", "")).upper()
                in ["MISSED", "DEFAULTED"]
            ),
        },

        "financial_features": (
            {
                "avg_monthly_income": features.avg_monthly_income,
                "avg_monthly_spending": features.avg_monthly_spending,
                "savings_rate": features.savings_rate,
                "cash_buffer": features.cash_buffer,
                "emi_ratio": features.emi_ratio,
                "credit_utilization": features.credit_utilization,
                "missed_emi_count": features.missed_emi_count,
                "transaction_frequency": features.transaction_frequency,
                "spending_growth": features.spending_growth,
                "balance_volatility": features.balance_volatility,
                "income_stability": features.income_stability,
            }
            if features
            else None
        ),

        "financial_health": (
            {
                "score": health.score,
                "level": health.health_level,
                "income_score": health.income_score,
                "spending_score": health.spending_score,
                "savings_score": health.savings_score,
                "debt_score": health.debt_score,
                "stability_score": health.stability_score,
                "strengths": health.strengths,
                "weaknesses": health.weaknesses,
                "recommendations": health.recommendations,
            }
            if health
            else None
        ),

        "financial_stress": (
            {
                "score": getattr(
                    stress,
                    "stress_score",
                    getattr(stress, "score", None),
                ),
                "level": getattr(
                    stress,
                    "stress_level",
                    getattr(stress, "level", None),
                ),
                "factors": getattr(
                    stress,
                    "stress_factors",
                    getattr(stress, "factors", None),
                ),
            }
            if stress
            else None
        ),
    }
