from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.privacy.consent_manager import (
    get_consent,
    grant_consent,
    revoke_consent,
)

router = APIRouter(tags=["Consent"])


class ConsentRequest(BaseModel):
    purpose: str
    granted: bool


@router.get("/customers/{customer_id}/data-consent")
def get_customer_consent(
    customer_id: int,
    db: Session = Depends(get_db),
):
    """
    Return all consent records for a customer.
    """

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )

    records = get_consent(
        db=db,
        customer_id=customer_id,
    )

    return {
        "success": True,
        "customer_id": customer_id,
        "consents": records,
    }


@router.post("/customers/{customer_id}/consent")
def update_customer_consent(
    customer_id: int,
    request: ConsentRequest,
    db: Session = Depends(get_db),
):
    """
    Grant or revoke consent for a specific purpose.
    """

    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found.",
        )

    if not request.purpose.strip():
        raise HTTPException(
            status_code=400,
            detail="Purpose cannot be empty.",
        )

    purpose = request.purpose.strip().lower()

    allowed_purposes = {
        "financial_analysis",
        "financial_advice",
        "loan_recommendation",
        "fraud_detection",
    }

    if purpose not in allowed_purposes:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Unsupported consent purpose.",
                "allowed_purposes": sorted(allowed_purposes),
            },
        )

    if request.granted:
        result = grant_consent(
            db=db,
            customer_id=customer_id,
            purpose=purpose,
        )
    else:
        result = revoke_consent(
            db=db,
            customer_id=customer_id,
            purpose=purpose,
        )

    return {
        "success": True,
        "message": (
            "Consent granted."
            if request.granted
            else "Consent revoked."
        ),
        "consent": result,
    }