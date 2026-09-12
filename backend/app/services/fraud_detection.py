from datetime import datetime

import numpy as np
from sqlalchemy.orm import Session

from app.models import (
    Customer,
    Transaction,
    FraudEvent,
)


# ============================================================
# FRAUD DETECTION ENGINE
# ============================================================


def calculate_transaction_fraud_score(
    transaction,
    customer_transactions,
):
    """
    Calculate a 0-100 fraud score for one transaction.

    This is a hybrid:
        - amount anomaly
        - frequency anomaly
        - location anomaly
        - device anomaly
        - beneficiary anomaly
        - transaction rules
    """

    amount = float(
        transaction.amount or 0
    )

    # --------------------------------------------------------
    # Historical transactions
    # --------------------------------------------------------

    historical = [
        t for t in customer_transactions
        if t.id != transaction.id
    ]

    if historical:

        historical_amounts = np.array(
            [
                float(t.amount)
                for t in historical
                if t.amount is not None
            ]
        )

    else:

        historical_amounts = np.array([])

    # ========================================================
    # 1. AMOUNT ANOMALY — 30 points
    # ========================================================

    if len(historical_amounts) >= 3:

        mean_amount = np.mean(
            historical_amounts
        )

        std_amount = np.std(
            historical_amounts
        )

        if std_amount > 0:

            z_score = abs(
                amount - mean_amount
            ) / std_amount

        else:

            z_score = 0

    else:

        mean_amount = amount
        z_score = 0

    if z_score >= 5:

        amount_score = 30

    elif z_score >= 3:

        amount_score = 25

    elif z_score >= 2:

        amount_score = 18

    elif z_score >= 1:

        amount_score = 10

    else:

        amount_score = 0

    # ========================================================
    # 2. TRANSACTION FREQUENCY — 15 points
    # ========================================================

    frequency_score = 0

    if historical:

        recent_transactions = [
            t for t in historical
            if t.timestamp
            and transaction.timestamp
            and abs(
                (
                    transaction.timestamp
                    - t.timestamp
                ).total_seconds()
            ) <= 3600
        ]

        recent_count = len(
            recent_transactions
        )

        if recent_count >= 10:

            frequency_score = 15

        elif recent_count >= 6:

            frequency_score = 10

        elif recent_count >= 4:

            frequency_score = 6

        elif recent_count >= 2:

            frequency_score = 3

    # ========================================================
    # 3. LOCATION ANOMALY — 20 points
    # ========================================================

    location_score = 0

    if historical:

        locations = [
            str(t.location).lower()
            for t in historical
            if t.location
        ]

        current_location = str(
            transaction.location
        ).lower()

        if locations:

            location_counts = {}

            for location in locations:

                location_counts[
                    location
                ] = (
                    location_counts.get(
                        location,
                        0,
                    )
                    + 1
                )

            common_location = max(
                location_counts,
                key=location_counts.get,
            )

            if (
                current_location
                != common_location
            ):

                location_score = 20

    # ========================================================
    # 4. DEVICE ANOMALY — 15 points
    # ========================================================

    device_score = 0

    if historical:

        known_devices = {
            str(t.device_id)
            for t in historical
            if t.device_id
        }

        current_device = str(
            transaction.device_id
        )

        if (
            current_device
            and current_device not in known_devices
        ):

            device_score = 15

    # ========================================================
    # 5. BENEFICIARY ANOMALY — 10 points
    # ========================================================

    beneficiary_score = 0

    current_beneficiary = (
        transaction.beneficiary
    )

    if current_beneficiary:

        known_beneficiaries = {
            str(t.beneficiary)
            for t in historical
            if t.beneficiary
        }

        if (
            str(current_beneficiary)
            not in known_beneficiaries
        ):

            beneficiary_score = 10

    # ========================================================
    # 6. RULE SCORE — 10 points
    # ========================================================

    rule_score = 0

    reasons = []

    # Large transaction
    if amount >= 100000:

        rule_score += 4

        reasons.append(
            "Very large transaction"
        )

    elif amount >= 50000:

        rule_score += 2

        reasons.append(
            "Large transaction"
        )

    # Round-number transaction
    if amount > 10000 and amount % 10000 == 0:

        rule_score += 2

        reasons.append(
            "Unusual round-number amount"
        )

    # New beneficiary
    if beneficiary_score > 0:

        rule_score += 2

        reasons.append(
            "New beneficiary"
        )

    # New device
    if device_score > 0:

        rule_score += 2

        reasons.append(
            "New device"
        )

    rule_score = min(
        rule_score,
        10,
    )

    # ========================================================
    # TOTAL FRAUD SCORE
    # ========================================================

    fraud_score = (
        amount_score
        + frequency_score
        + location_score
        + device_score
        + beneficiary_score
        + rule_score
    )

    fraud_score = max(
        0,
        min(
            100,
            round(fraud_score),
        ),
    )

    # ========================================================
    # RISK LEVEL
    # ========================================================

    if fraud_score >= 75:

        risk_level = "CRITICAL"

        recommended_action = (
            "BLOCK_TRANSACTION"
        )

    elif fraud_score >= 50:

        risk_level = "HIGH"

        recommended_action = (
            "STEP_UP_AUTHENTICATION"
        )

    elif fraud_score >= 30:

        risk_level = "MEDIUM"

        recommended_action = (
            "REVIEW_TRANSACTION"
        )

    else:

        risk_level = "LOW"

        recommended_action = (
            "ALLOW_TRANSACTION"
        )

    # ========================================================
    # Automatic explanations
    # ========================================================

    if z_score >= 3:

        reasons.append(
            "Transaction amount is highly unusual"
        )

    if frequency_score >= 10:

        reasons.append(
            "Unusually high transaction frequency"
        )

    if location_score > 0:

        reasons.append(
            "Transaction location differs from normal pattern"
        )

    if device_score > 0:

        reasons.append(
            "Transaction originated from a new device"
        )

    if not reasons:

        reasons.append(
            "No significant fraud indicators detected"
        )

    return {
        "fraud_score": fraud_score,
        "risk_level": risk_level,
        "reason": "; ".join(reasons),
        "anomaly_score": round(
            min(z_score / 5, 1),
            4,
        ),
        "rule_score": rule_score,
        "identity_risk_score": round(
            (
                device_score
                + beneficiary_score
            ) / 25,
            4,
        ),
        "recommended_action": (
            recommended_action
        ),
    }


# ============================================================
# ANALYZE TRANSACTION
# ============================================================


def analyze_transaction(
    db: Session,
    transaction_id: int,
):
    """
    Analyze one transaction for fraud.
    """

    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id
        )
        .first()
    )

    if not transaction:

        raise ValueError(
            f"Transaction {transaction_id} "
            f"not found"
        )

    customer_transactions = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id
            == transaction.customer_id
        )
        .all()
    )

    result = calculate_transaction_fraud_score(
        transaction,
        customer_transactions,
    )

    # --------------------------------------------------------
    # Save fraud event
    # --------------------------------------------------------

    fraud_event = FraudEvent(
        customer_id=transaction.customer_id,

        transaction_id=transaction.id,

        fraud_score=result[
            "fraud_score"
        ],

        risk_level=result[
            "risk_level"
        ],

        status="OPEN"
        if result["fraud_score"] >= 30
        else "CLOSED",

        reason=result[
            "reason"
        ],

        anomaly_score=result[
            "anomaly_score"
        ],

        rule_score=result[
            "rule_score"
        ],

        identity_risk_score=result[
            "identity_risk_score"
        ],

        recommended_action=result[
            "recommended_action"
        ],
    )

    db.add(fraud_event)

    db.commit()

    db.refresh(fraud_event)

    return fraud_event


# ============================================================
# ANALYZE ALL TRANSACTIONS
# ============================================================


def analyze_all_transactions(
    db: Session,
    limit=None,
):
    """
    Analyze transactions for fraud.

    Existing fraud events generated by the
    synthetic-data generator are preserved.
    """

    query = (
        db.query(Transaction)
        .order_by(Transaction.id)
    )

    if limit:

        query = query.limit(limit)

    transactions = query.all()

    print(
        f"\nAnalyzing {len(transactions)} "
        f"transactions for fraud..."
    )

    results = []

    for transaction in transactions:

        try:

            # ------------------------------------------------
            # Get customer transactions
            # ------------------------------------------------

            customer_transactions = (
                db.query(Transaction)
                .filter(
                    Transaction.customer_id
                    == transaction.customer_id
                )
                .all()
            )

            result = (
                calculate_transaction_fraud_score(
                    transaction,
                    customer_transactions,
                )
            )

            results.append(
                (
                    transaction,
                    result,
                )
            )

            if result["fraud_score"] >= 30:

                print(
                    f"⚠ Transaction "
                    f"{transaction.id}: "
                    f"{result['fraud_score']}/100 "
                    f"({result['risk_level']})"
                )

        except Exception as exc:

            print(
                f"✗ Transaction "
                f"{transaction.id} failed: "
                f"{exc}"
            )

    return results


# ============================================================
# SAVE BATCH RESULTS
# ============================================================


def save_fraud_results(
    db: Session,
    results,
):
    """
    Save fraud analysis results.
    """

    saved = 0

    for transaction, result in results:

        fraud_event = FraudEvent(
            customer_id=transaction.customer_id,

            transaction_id=transaction.id,

            fraud_score=result[
                "fraud_score"
            ],

            risk_level=result[
                "risk_level"
            ],

            status="OPEN"
            if result["fraud_score"] >= 30
            else "CLOSED",

            reason=result[
                "reason"
            ],

            anomaly_score=result[
                "anomaly_score"
            ],

            rule_score=result[
                "rule_score"
            ],

            identity_risk_score=result[
                "identity_risk_score"
            ],

            recommended_action=result[
                "recommended_action"
            ],
        )

        db.add(fraud_event)

        saved += 1

    db.commit()

    return saved