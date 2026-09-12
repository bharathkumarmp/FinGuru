from datetime import datetime, timedelta
from statistics import mean, pstdev
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def _safe_mean(values: List[float]) -> float:
    return mean(values) if values else 0.0


def _safe_std(values: List[float]) -> float:
    if len(values) < 2:
        return 0.0
    return pstdev(values)


def detect_transaction_anomaly(
    db: Session,
    customer_id: int,
    transaction_id: int,
) -> Dict[str, Any]:
    """
    Detect transaction-level anomalies using the customer's
    historical transaction behavior.

    This service is intentionally independent from fraud_detection.py.
    It identifies unusual transaction behavior; the fraud engine can
    subsequently use this signal as part of the overall risk decision.
    """

    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.customer_id == customer_id,
        )
        .first()
    )

    if not transaction:
        raise ValueError(
            f"Transaction {transaction_id} not found for customer {customer_id}."
        )

    historical_transactions = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer_id,
            Transaction.id != transaction_id,
        )
        .order_by(Transaction.timestamp.desc())
        .limit(100)
        .all()
    )

    amounts = [
        float(tx.amount)
        for tx in historical_transactions
        if tx.amount is not None
    ]

    avg_amount = _safe_mean(amounts)
    std_amount = _safe_std(amounts)

    if std_amount > 0:
        amount_zscore = abs(
            (float(transaction.amount) - avg_amount) / std_amount
        )
    else:
        amount_zscore = 0.0

    # ---------------------------------------------------------
    # Amount anomaly
    # ---------------------------------------------------------

    amount_anomaly = amount_zscore >= 3.0

    # ---------------------------------------------------------
    # Merchant anomaly
    # ---------------------------------------------------------

    historical_merchants = {
        tx.merchant
        for tx in historical_transactions
        if tx.merchant
    }

    merchant_anomaly = (
        transaction.merchant is not None
        and transaction.merchant not in historical_merchants
        and len(historical_merchants) > 0
    )

    # ---------------------------------------------------------
    # Location anomaly
    # ---------------------------------------------------------

    historical_locations = {
        tx.location
        for tx in historical_transactions
        if tx.location
    }

    location_anomaly = (
        transaction.location is not None
        and transaction.location not in historical_locations
        and len(historical_locations) > 0
    )

    # ---------------------------------------------------------
    # Device anomaly
    # ---------------------------------------------------------

    historical_devices = {
        tx.device_id
        for tx in historical_transactions
        if tx.device_id
    }

    device_anomaly = (
        transaction.device_id is not None
        and transaction.device_id not in historical_devices
        and len(historical_devices) > 0
    )

    # ---------------------------------------------------------
    # Beneficiary anomaly
    # ---------------------------------------------------------

    historical_beneficiaries = {
        tx.beneficiary
        for tx in historical_transactions
        if tx.beneficiary
    }

    beneficiary_anomaly = (
        transaction.beneficiary is not None
        and transaction.beneficiary not in historical_beneficiaries
        and len(historical_beneficiaries) > 0
    )

    # ---------------------------------------------------------
    # Recent transaction frequency
    # ---------------------------------------------------------

    now = transaction.timestamp or datetime.utcnow()
    recent_start = now - timedelta(hours=24)

    recent_transactions = [
        tx
        for tx in historical_transactions
        if tx.timestamp and tx.timestamp >= recent_start
    ]

    recent_frequency = len(recent_transactions)

    # A very high number of transactions in 24 hours is suspicious.
    frequency_anomaly = recent_frequency >= 15

    # ---------------------------------------------------------
    # Anomaly scoring
    # ---------------------------------------------------------

    signals = {
        "amount_anomaly": amount_anomaly,
        "merchant_anomaly": merchant_anomaly,
        "location_anomaly": location_anomaly,
        "device_anomaly": device_anomaly,
        "beneficiary_anomaly": beneficiary_anomaly,
        "frequency_anomaly": frequency_anomaly,
    }

    weights = {
        "amount_anomaly": 30,
        "merchant_anomaly": 15,
        "location_anomaly": 15,
        "device_anomaly": 15,
        "beneficiary_anomaly": 15,
        "frequency_anomaly": 10,
    }

    anomaly_score = sum(
        weights[name]
        for name, triggered in signals.items()
        if triggered
    )

    anomaly_score = min(anomaly_score, 100)

    if anomaly_score >= 75:
        risk_level = "CRITICAL"
    elif anomaly_score >= 50:
        risk_level = "HIGH"
    elif anomaly_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if anomaly_score >= 75:
        recommended_action = "BLOCK_AND_ESCALATE"
    elif anomaly_score >= 50:
        recommended_action = "STEP_UP_AUTHENTICATION"
    elif anomaly_score >= 30:
        recommended_action = "REVIEW_TRANSACTION"
    else:
        recommended_action = "ALLOW_TRANSACTION"

    triggered_signals = [
        name
        for name, triggered in signals.items()
        if triggered
    ]

    if triggered_signals:
        reason = (
            "Transaction anomaly detected: "
            + ", ".join(triggered_signals)
            + "."
        )
    else:
        reason = "Transaction behavior is consistent with historical activity."

    return {
        "customer_id": customer_id,
        "transaction_id": transaction_id,
        "anomaly_score": round(anomaly_score, 2),
        "risk_level": risk_level,
        "recommended_action": recommended_action,
        "reason": reason,
        "signals": signals,
        "triggered_signals": triggered_signals,
        "transaction": {
            "amount": float(transaction.amount),
            "merchant": transaction.merchant,
            "category": transaction.category,
            "location": transaction.location,
            "device_id": transaction.device_id,
            "beneficiary": transaction.beneficiary,
            "timestamp": transaction.timestamp,
        },
        "baseline": {
            "historical_transaction_count": len(historical_transactions),
            "average_transaction_amount": round(avg_amount, 2),
            "transaction_amount_std": round(std_amount, 2),
            "amount_zscore": round(amount_zscore, 2),
            "recent_24h_transaction_count": recent_frequency,
        },
        "calculated_at": datetime.utcnow(),
    }