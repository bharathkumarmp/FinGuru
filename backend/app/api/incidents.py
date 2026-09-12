from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import Incident

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.get("")
def get_incidents(
    db: Session = Depends(get_db),
):
    incidents = (
        db.query(Incident)
        .order_by(Incident.detected_at.desc())
        .all()
    )

    return {
        "success": True,
        "count": len(incidents),
        "data": [
            {
                "id": incident.id,
                "incident_type": incident.incident_type,
                "severity": incident.severity,
                "customer_id": incident.customer_id,
                "title": incident.title,
                "description": incident.description,
                "status": incident.status,
                "recommended_action": incident.recommended_action,
                "detected_at": incident.detected_at,
                "resolved_at": incident.resolved_at,
            }
            for incident in incidents
        ],
    }


@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail=f"Incident {incident_id} not found",
        )

    return {
        "success": True,
        "data": {
            "id": incident.id,
            "incident_type": incident.incident_type,
            "severity": incident.severity,
            "customer_id": incident.customer_id,
            "title": incident.title,
            "description": incident.description,
            "status": incident.status,
            "recommended_action": incident.recommended_action,
            "detected_at": incident.detected_at,
            "resolved_at": incident.resolved_at,
        },
    }