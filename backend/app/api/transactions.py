from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Transaction


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


# ============================================================
# REQUEST SCHEMA
# ============================================================

class TransactionCreate(BaseModel):
    customer_id: int = Field(..., gt=0)

    account_id: Optional[int] = None

    transaction_type: str

    amount: float = Field(..., gt=0)

    merchant: Optional[str] = None

    category: Optional[str] = None

    location: Optional[str] = None

    device_id: Optional[str] = None

    beneficiary: Optional[str] = None

    description: Optional[str] = None

    timestamp: Optional[datetime] = None


# ============================================================
# TRANSACTION RESPONSE
# ============================================================

def transaction_to_dict(
    transaction: Transaction,
) -> dict:

    return {
        "id": transaction.id,
        "customer_id": transaction.customer_id,
        "account_id": transaction.account_id,
        "transaction_type": transaction.transaction_type,
        "amount": float(transaction.amount),
        "merchant": transaction.merchant,
        "category": transaction.category,
        "location": transaction.location,
        "device_id": transaction.device_id,
        "beneficiary": transaction.beneficiary,
        "description": transaction.description,
        "timestamp": transaction.timestamp,
    }


# ============================================================
# GET CUSTOMER TRANSACTIONS
# ============================================================

@router.get("/customer/{customer_id}")
def get_customer_transactions(
    customer_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Get recent transactions for a customer.
    """

    if limit < 1 or limit > 1000:

        raise HTTPException(
            status_code=400,
            detail="limit must be between 1 and 1000",
        )

    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.customer_id == customer_id
        )
        .order_by(
            Transaction.timestamp.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "success": True,
        "customer_id": customer_id,
        "count": len(transactions),
        "transactions": [
            transaction_to_dict(transaction)
            for transaction in transactions
        ],
    }


# ============================================================
# GET SINGLE TRANSACTION
# ============================================================

@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a single transaction.
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

    return {
        "success": True,
        "transaction": transaction_to_dict(
            transaction
        ),
    }


# ============================================================
# CREATE TRANSACTION
# ============================================================

@router.post("")
def create_transaction(
    request: TransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a banking transaction.

    This endpoint can later trigger:
    - Fraud Detection
    - Transaction Anomaly
    - UEBA
    - Identity Risk
    - Event Processing
    """

    transaction = Transaction(
        customer_id=request.customer_id,
        account_id=request.account_id,
        transaction_type=request.transaction_type,
        amount=Decimal(
            str(request.amount)
        ),
        merchant=request.merchant,
        category=request.category,
        location=request.location,
        device_id=request.device_id,
        beneficiary=request.beneficiary,
        description=request.description,
        timestamp=(
            request.timestamp
            if request.timestamp
            else datetime.utcnow()
        ),
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return {
        "success": True,
        "message": "Transaction created successfully",
        "transaction": transaction_to_dict(
            transaction
        ),
    }