from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.account import Account
from app.models.transaction import Transaction


def calculate_identity_risk(
    new_device: bool,
    new_location: bool,
    new_beneficiary: bool,
    unusual_transaction: bool,
    inactive_account: bool,
) -> float:
    """
    Calculate identity/account takeover risk.

    This is a prototype risk-scoring engine.
    """

    score = 0.0

    if new_device:
        score += 25

    if new_location:
        score += 20

    if new_beneficiary:
        score += 25

    if unusual_transaction:
        score += 20

    if inactive_account:
        score += 10

    return round(min(score, 100), 2)


def analyze_identity_risk(
    db: Session,
    customer_id: int,
    transaction_id: int | None = None,
) -> Dict[str, Any]:

    # ---------------------------------------------------------
    # Customer
    # ---------------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise ValueError(
            f"Customer {customer_id} not found"
        )

    # ---------------------------------------------------------
    # Accounts
    # ---------------------------------------------------------

    accounts = (
        db.query(Account)
        .filter(Account.customer_id == customer_id)
        .all()
    )

    if not accounts:
        return {
            "customer_id": customer_id,
            "identity_status": "NO_ACCOUNT",
            "identity_risk_score": 0,
            "risk_level": "LOW",
            "signals": {},
            "reasons": [
                "No account information available."
            ],
        }

    # ---------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------

    transactions = (
        db.query(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    if not transactions:
        return {
            "customer_id": customer_id,
            "identity_status": "NO_TRANSACTION_DATA",
            "identity_risk_score": 0,
            "risk_level": "LOW",
            "signals": {},
            "reasons": [
                "No transaction history available."
            ],
        }

    # ---------------------------------------------------------
    # Target transaction
    # ---------------------------------------------------------

    target = None

    if transaction_id is not None:
        for transaction in transactions:
            if transaction.id == transaction_id:
                target = transaction
                break

    if target is None:
        target = transactions[0]

    historical = [
        transaction
        for transaction in transactions
        if transaction.id != target.id
    ]

    # ---------------------------------------------------------
    # Device signal
    # ---------------------------------------------------------

    historical_devices = {
        transaction.device_id
        for transaction in historical
        if transaction.device_id
    }

    new_device = (
        bool(target.device_id)
        and target.device_id not in historical_devices
    )

    # ---------------------------------------------------------
    # Location signal
    # ---------------------------------------------------------

    historical_locations = {
        transaction.location
        for transaction in historical
        if transaction.location
    }

    new_location = (
        bool(target.location)
        and target.location not in historical_locations
    )

    # ---------------------------------------------------------
    # Beneficiary signal
    # ---------------------------------------------------------

    historical_beneficiaries = {
        transaction.beneficiary
        for transaction in historical
        if transaction.beneficiary
    }

    new_beneficiary = (
        bool(target.beneficiary)
        and target.beneficiary not in historical_beneficiaries
    )

    # ---------------------------------------------------------
    # Transaction anomaly
    # ---------------------------------------------------------

    amounts = [
        float(transaction.amount or 0)
        for transaction in historical
        if float(transaction.amount or 0) > 0
    ]

    target_amount = float(target.amount or 0)

    if amounts:
        average_amount = sum(amounts) / len(amounts)

        unusual_transaction = (
            target_amount > average_amount * 3
        )
    else:
        average_amount = target_amount
        unusual_transaction = False

    # ---------------------------------------------------------
    # Account status
    # ---------------------------------------------------------

    active_accounts = [
        account
        for account in accounts
        if str(account.status).upper() == "ACTIVE"
    ]

    inactive_account = len(active_accounts) == 0

    # ---------------------------------------------------------
    # Risk score
    # ---------------------------------------------------------

    risk_score = calculate_identity_risk(
        new_device=new_device,
        new_location=new_location,
        new_beneficiary=new_beneficiary,
        unusual_transaction=unusual_transaction,
        inactive_account=inactive_account,
    )

    # ---------------------------------------------------------
    # Risk level
    # ---------------------------------------------------------

    if risk_score >= 75:
        risk_level = "CRITICAL"
    elif risk_score >= 50:
        risk_level = "HIGH"
    elif risk_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    reasons = []

    if new_device:
        reasons.append(
            "Transaction originated from a new device."
        )

    if new_location:
        reasons.append(
            "Transaction originated from a new location."
        )

    if new_beneficiary:
        reasons.append(
            "Transaction involves a new beneficiary."
        )

    if unusual_transaction:
        reasons.append(
            "Transaction amount is unusually high compared "
            "with historical customer behavior."
        )

    if inactive_account:
        reasons.append(
            "Customer has no active account."
        )

    if not reasons:
        reasons.append(
            "No significant identity-risk signals detected."
        )

    return {
        "customer_id": customer_id,
        "transaction_id": target.id,
        "identity_status": (
            "HIGH_RISK"
            if risk_score >= 50
            else "NORMAL"
        ),
        "identity_risk_score": risk_score,
        "risk_level": risk_level,
        "signals": {
            "new_device": new_device,
            "new_location": new_location,
            "new_beneficiary": new_beneficiary,
            "unusual_transaction": unusual_transaction,
            "inactive_account": inactive_account,
        },
        "baseline": {
            "historical_devices": len(
                historical_devices
            ),
            "historical_locations": len(
                historical_locations
            ),
            "historical_beneficiaries": len(
                historical_beneficiaries
            ),
            "average_transaction_amount": round(
                average_amount,
                2,
            ),
        },
        "reasons": reasons,
    }