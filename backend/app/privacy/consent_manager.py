from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.consent import Consent


def grant_consent(
    db: Session,
    customer_id: int,
    purpose: str,
) -> Dict[str, Any]:
    """
    Grant consent for a specific purpose.

    If consent already exists for the customer and purpose,
    update it instead of creating a duplicate record.
    """

    consent = (
        db.query(Consent)
        .filter(
            Consent.customer_id == customer_id,
            Consent.purpose == purpose,
        )
        .first()
    )

    if consent:
        consent.granted = True
        consent.updated_at = datetime.utcnow()
    else:
        consent = Consent(
            customer_id=customer_id,
            purpose=purpose,
            granted=True,
        )
        db.add(consent)

    db.commit()
    db.refresh(consent)

    return {
        "id": consent.id,
        "customer_id": consent.customer_id,
        "purpose": consent.purpose,
        "granted": consent.granted,
        "created_at": consent.created_at,
        "updated_at": consent.updated_at,
    }


def revoke_consent(
    db: Session,
    customer_id: int,
    purpose: str,
) -> Dict[str, Any]:
    """
    Revoke consent for a specific purpose.
    """

    consent = (
        db.query(Consent)
        .filter(
            Consent.customer_id == customer_id,
            Consent.purpose == purpose,
        )
        .first()
    )

    if not consent:
        return {
            "customer_id": customer_id,
            "purpose": purpose,
            "granted": False,
            "message": "No consent record found. Consent remains unavailable.",
        }

    consent.granted = False
    consent.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(consent)

    return {
        "id": consent.id,
        "customer_id": consent.customer_id,
        "purpose": consent.purpose,
        "granted": consent.granted,
        "created_at": consent.created_at,
        "updated_at": consent.updated_at,
    }


def has_consent(
    db: Session,
    customer_id: int,
    purpose: str,
) -> bool:
    """
    Check whether a customer has currently granted
    consent for a specific purpose.
    """

    consent = (
        db.query(Consent)
        .filter(
            Consent.customer_id == customer_id,
            Consent.purpose == purpose,
            Consent.granted.is_(True),
        )
        .first()
    )

    return consent is not None


def get_consent(
    db: Session,
    customer_id: int,
    purpose: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieve consent records for a customer.

    If purpose is provided, return only that purpose.
    """

    query = db.query(Consent).filter(
        Consent.customer_id == customer_id
    )

    if purpose:
        query = query.filter(Consent.purpose == purpose)

    records = query.order_by(Consent.updated_at.desc()).all()

    return [
        {
            "id": consent.id,
            "customer_id": consent.customer_id,
            "purpose": consent.purpose,
            "granted": consent.granted,
            "created_at": consent.created_at,
            "updated_at": consent.updated_at,
        }
        for consent in records
    ]