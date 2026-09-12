from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Account, Customer


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


# ============================================================
# SERIALIZER
# ============================================================

def account_to_dict(account: Account) -> dict:
    """
    Convert Account SQLAlchemy object into a JSON-safe dict.
    """

    return {
        "id": account.id,
        "customer_id": account.customer_id,
        "account_number": account.account_number,
        "account_type": account.account_type,
        "balance": float(account.balance),
        "currency": account.currency,
        "status": account.status,
        "created_at": account.created_at,
    }


# ============================================================
# GET SINGLE ACCOUNT
# ============================================================

@router.get("/{account_id}")
def get_account(
    account_id: int,
    db: Session = Depends(get_db),
):
    """
    Get details of a single bank account.
    """

    account = (
        db.query(Account)
        .filter(
            Account.id == account_id
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found",
        )

    return {
        "success": True,
        "account": account_to_dict(account),
    }


# ============================================================
# GET CUSTOMER ACCOUNTS
# ============================================================

@router.get("/customer/{customer_id}")
def get_customer_accounts(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Get all accounts belonging to a customer.
    """

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    accounts = (
        db.query(Account)
        .filter(
            Account.customer_id == customer_id
        )
        .order_by(
            Account.id.asc()
        )
        .all()
    )

    total_balance = sum(
        (
            account.balance
            for account in accounts
            if account.balance is not None
        ),
        Decimal("0"),
    )

    return {
        "success": True,
        "customer_id": customer_id,
        "count": len(accounts),
        "total_balance": float(total_balance),
        "currency": (
            accounts[0].currency
            if accounts
            else "INR"
        ),
        "accounts": [
            account_to_dict(account)
            for account in accounts
        ],
    }


# ============================================================
# ACCOUNT BALANCE
# ============================================================

@router.get("/{account_id}/balance")
def get_account_balance(
    account_id: int,
    db: Session = Depends(get_db),
):
    """
    Get the current balance of an account.
    """

    account = (
        db.query(Account)
        .filter(
            Account.id == account_id
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=404,
            detail=f"Account {account_id} not found",
        )

    return {
        "success": True,
        "account_id": account.id,
        "account_number": account.account_number,
        "balance": float(account.balance),
        "currency": account.currency,
        "status": account.status,
    }


# ============================================================
# CUSTOMER TOTAL BALANCE
# ============================================================

@router.get("/customer/{customer_id}/balance")
def get_customer_balance(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Calculate the customer's total balance across accounts.
    """

    customer = (
        db.query(Customer)
        .filter(
            Customer.id == customer_id
        )
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail=f"Customer {customer_id} not found",
        )

    accounts = (
        db.query(Account)
        .filter(
            Account.customer_id == customer_id
        )
        .all()
    )

    total_balance = sum(
        (
            account.balance
            for account in accounts
            if account.balance is not None
        ),
        Decimal("0"),
    )

    return {
        "success": True,
        "customer_id": customer_id,
        "account_count": len(accounts),
        "total_balance": float(total_balance),
        "currency": (
            accounts[0].currency
            if accounts
            else "INR"
        ),
    }