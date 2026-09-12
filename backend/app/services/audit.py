import json
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_audit_log(
    db: Session,
    action: str,
    resource: str | None = None,
    user_id: int | None = None,
    customer_id: int | None = None,
    ip_address: str | None = None,
    details: dict[str, Any] | str | None = None,
) -> AuditLog:
    """
    Create an immutable-style audit record for a security
    or financial action.
    """

    if isinstance(details, dict):
        details_value = json.dumps(
            details,
            default=str,
        )
    elif details is None:
        details_value = None
    else:
        details_value = str(details)

    audit = AuditLog(
        user_id=user_id,
        customer_id=customer_id,
        action=action,
        resource=resource,
        ip_address=ip_address,
        details=details_value,
        created_at=datetime.utcnow(),
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

    return audit


def audit_incident_action(
    db: Session,
    customer_id: int,
    incident_id: int,
    action: str,
    details: dict[str, Any] | None = None,
) -> AuditLog:
    """
    Convenience function for incident-related audit events.
    """

    return create_audit_log(
        db=db,
        action=action,
        resource=f"incident:{incident_id}",
        customer_id=customer_id,
        details=details,
    )