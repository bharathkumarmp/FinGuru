from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Customer, Transaction
from app.services.fraud_detection import (
    analyze_transaction,
    analyze_all_transactions,
    save_fraud_results,
)


router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Detection"],
)


# ============================================================
# REQUEST SCHEMAS
# ============================================================

class FraudAnalyzeRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    transaction_id: int = Field(..., gt=0)


class FraudBatchRequest(BaseModel):
    limit: int = Field(default=100, ge=1, le=1000)


# ============================================================
# SERIALIZER
# ============================================================

def fraud_to_dict(result) -> dict:
    """
    Convert FraudEvent SQLAlchemy object or dictionary
    into a JSON-safe response.
    """

    if isinstance(result, dict):
        data = result
    else:
        data = {
            column.name: getattr(result, column.name)
            for column in result.__table__.columns
        }

    return {
        "id": data.get("id"),
        "customer_id": data.get("customer_id"),
        "transaction_id": data.get("transaction_id"),

        "fraud_score": (
            float(data["fraud_score"])
            if data.get("fraud_score") is not None
            else 0.0
        ),

        "risk_level": data.get("risk_level"),

        "reason": data.get("reason"),

        "anomaly_score": (
            float(data["anomaly_score"])
            if data.get("anomaly_score") is not None
            else 0.0
        ),

        "rule_score": (
            float(data["rule_score"])
            if data.get("rule_score") is not None
            else 0.0
        ),

        "identity_risk_score": (
            float(data["identity_risk_score"])
            if data.get("identity_risk_score") is not None
            else 0.0
        ),

        "recommended_action": data.get(
            "recommended_action"
        ),
    }


# ============================================================
# ANALYZE SINGLE TRANSACTION
# ============================================================

@router.post("/analyze")
def analyze_fraud(
    request: FraudAnalyzeRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze one transaction for fraud.

    Flow:

    Transaction
        ↓
    Fraud Detection
        ↓
    Fraud Score
        ↓
    Risk Level
        ↓
    Recommended Action
    """

    # --------------------------------------------------------
    # CHECK CUSTOMER
    # --------------------------------------------------------

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == request.customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Customer "
                f"{request.customer_id} not found"
            ),
        )

    # --------------------------------------------------------
    # CHECK TRANSACTION
    # --------------------------------------------------------

    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == request.transaction_id,
            Transaction.customer_id == request.customer_id,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Transaction "
                f"{request.transaction_id} not found "
                f"for customer "
                f"{request.customer_id}"
            ),
        )

    # --------------------------------------------------------
    # ANALYZE
    # --------------------------------------------------------

    try:

        result = analyze_transaction(
            db=db,
            transaction_id=request.transaction_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Fraud analysis failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "customer_id": request.customer_id,
        "transaction_id": request.transaction_id,
        "fraud_analysis": fraud_to_dict(result),
    }


# ============================================================
# ANALYZE ALL / BATCH
# ============================================================

@router.post("/analyze-batch")
def analyze_fraud_batch(
    request: FraudBatchRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze a batch of transactions.

    Useful for:
    - Initial model evaluation
    - Demonstration
    - Batch fraud scanning
    - Background processing
    """

    try:

        results = analyze_all_transactions(
            db=db,
            limit=request.limit,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Batch fraud analysis failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------------

    try:

        saved_results = save_fraud_results(
            db=db,
            results=results,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Saving fraud results failed: "
                f"{exc}"
            ),
        )

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "success": True,
        "message": "Batch fraud analysis completed",
        "analyzed_count": len(results),
        "saved_count": len(saved_results),
        "results": [
            fraud_to_dict(result)
            for result in saved_results
        ],
    }


# ============================================================
# GET TRANSACTION FRAUD RESULT
# ============================================================

@router.get("/transaction/{transaction_id}")
def get_transaction_fraud(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """
    Analyze a transaction and return its fraud result.
    """

    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Transaction "
                f"{transaction_id} not found"
            ),
        )

    try:

        result = analyze_transaction(
            db=db,
            transaction_id=transaction_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Fraud analysis failed: "
                f"{exc}"
            ),
        )

    return {
        "success": True,
        "transaction_id": transaction_id,
        "fraud_analysis": fraud_to_dict(result),
    }