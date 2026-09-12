from datetime import datetime, timedelta
from statistics import mean, stdev
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models.transaction import Transaction


def calculate_ueba_score(
    amount_zscore: float,
    frequency_deviation: float,
    location_anomaly: float,
    device_anomaly: float,
    beneficiary_anomaly: float,
) -> float:
    """
    Calculate behavioral anomaly risk score.
    """

    score = (
        min(amount_zscore / 3.0, 1.0) * 30
        + frequency_deviation * 20
        + location_anomaly * 15
        + device_anomaly * 20
        + beneficiary_anomaly * 15
    )

    return round(max(0, min(100, score)), 2)


def analyze_customer_behavior(
    db: Session,
    customer_id: int,
    transaction_id: int | None = None,
) -> Dict[str, Any]:

    transactions = (
        db.query(Transaction)
        .filter(Transaction.customer_id == customer_id)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    if not transactions:
        return {
            "customer_id": customer_id,
            "behavior_status": "NO_DATA",
            "ueba_score": 0,
            "anomalies": [],
        }

    # ---------------------------------------------------------
    # Transaction being analyzed
    # ---------------------------------------------------------

    target = None

    if transaction_id is not None:
        for transaction in transactions:
            if transaction.id == transaction_id:
                target = transaction
                break

    if target is None:
        target = transactions[0]

    # ---------------------------------------------------------
    # Historical baseline
    # ---------------------------------------------------------

    historical = [
        transaction
        for transaction in transactions
        if transaction.id != target.id
    ]

    amounts = [
        float(transaction.amount or 0)
        for transaction in historical
        if float(transaction.amount or 0) > 0
    ]

    if not amounts:
        amounts = [float(target.amount or 0)]

    average_amount = mean(amounts)

    if len(amounts) > 1:
        std_amount = stdev(amounts)
    else:
        std_amount = 0

    target_amount = float(target.amount or 0)

    if std_amount > 0:
        amount_zscore = abs(
            target_amount - average_amount
        ) / std_amount
    else:
        amount_zscore = 0

    # ---------------------------------------------------------
    # Transaction frequency deviation
    # ---------------------------------------------------------

    recent_cutoff = datetime.utcnow() - timedelta(days=30)

    recent_transactions = [
        transaction
        for transaction in historical
        if transaction.timestamp
        and transaction.timestamp >= recent_cutoff
    ]

    historical_cutoff = datetime.utcnow() - timedelta(days=90)

    older_transactions = [
        transaction
        for transaction in historical
        if transaction.timestamp
        and transaction.timestamp >= historical_cutoff
    ]

    recent_frequency = len(recent_transactions)

    if older_transactions:
        baseline_frequency = len(older_transactions) / 3
    else:
        baseline_frequency = recent_frequency

    if baseline_frequency > 0:
        frequency_deviation = min(
            abs(recent_frequency - baseline_frequency)
            / baseline_frequency,
            1.0,
        )
    else:
        frequency_deviation = 0

    # ---------------------------------------------------------
    # Location anomaly
    # ---------------------------------------------------------

    locations = [
        transaction.location
        for transaction in historical
        if transaction.location
    ]

    target_location = target.location

    if target_location and locations:
        location_anomaly = (
            0 if target_location in locations else 1
        )
    else:
        location_anomaly = 0

    # ---------------------------------------------------------
    # Device anomaly
    # ---------------------------------------------------------

    devices = [
        transaction.device_id
        for transaction in historical
        if transaction.device_id
    ]

    target_device = target.device_id

    if target_device and devices:
        device_anomaly = (
            0 if target_device in devices else 1
        )
    else:
        device_anomaly = 0

    # ---------------------------------------------------------
    # Beneficiary anomaly
    # ---------------------------------------------------------

    beneficiaries = [
        transaction.beneficiary
        for transaction in historical
        if transaction.beneficiary
    ]

    target_beneficiary = target.beneficiary

    if target_beneficiary and beneficiaries:
        beneficiary_anomaly = (
            0
            if target_beneficiary in beneficiaries
            else 1
        )
    else:
        beneficiary_anomaly = 0

    # ---------------------------------------------------------
    # Overall UEBA score
    # ---------------------------------------------------------

    ueba_score = calculate_ueba_score(
        amount_zscore=amount_zscore,
        frequency_deviation=frequency_deviation,
        location_anomaly=location_anomaly,
        device_anomaly=device_anomaly,
        beneficiary_anomaly=beneficiary_anomaly,
    )

    # ---------------------------------------------------------
    # Risk classification
    # ---------------------------------------------------------

    if ueba_score >= 75:
        risk_level = "CRITICAL"
    elif ueba_score >= 50:
        risk_level = "HIGH"
    elif ueba_score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # ---------------------------------------------------------
    # Explainability
    # ---------------------------------------------------------

    anomalies = []

    if amount_zscore >= 2:
        anomalies.append(
            "Transaction amount is significantly different "
            "from historical behavior."
        )

    if frequency_deviation >= 0.5:
        anomalies.append(
            "Transaction frequency deviates from the customer's "
            "normal pattern."
        )

    if location_anomaly:
        anomalies.append(
            "Transaction originated from an unusual location."
        )

    if device_anomaly:
        anomalies.append(
            "Transaction originated from an unusual device."
        )

    if beneficiary_anomaly:
        anomalies.append(
            "Transaction involves a new or unusual beneficiary."
        )

    if not anomalies:
        anomalies.append(
            "Transaction behavior is consistent with the "
            "customer's historical pattern."
        )

    return {
        "customer_id": customer_id,
        "transaction_id": target.id,
        "behavior_status": (
            "ANOMALOUS"
            if ueba_score >= 30
            else "NORMAL"
        ),
        "ueba_score": ueba_score,
        "risk_level": risk_level,
        "baseline": {
            "average_transaction_amount": round(
                average_amount,
                2,
            ),
            "transaction_count": len(historical),
            "recent_30_day_frequency": recent_frequency,
        },
        "behavior_signals": {
            "amount_zscore": round(
                amount_zscore,
                2,
            ),
            "frequency_deviation": round(
                frequency_deviation,
                2,
            ),
            "location_anomaly": location_anomaly,
            "device_anomaly": device_anomaly,
            "beneficiary_anomaly": beneficiary_anomaly,
        },
        "anomalies": anomalies,
    }