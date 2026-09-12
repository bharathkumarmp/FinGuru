from datetime import datetime
from typing import Dict, Any

from sqlalchemy.orm import Session

from app.models.incident import Incident


def determine_severity(threat_score: float) -> str:
    if threat_score >= 75:
        return "CRITICAL"
    elif threat_score >= 50:
        return "HIGH"
    elif threat_score >= 30:
        return "MEDIUM"
    else:
        return "LOW"


def create_security_incident(
    db: Session,
    customer_id: int,
    threat_score: float,
    threat_level: str,
    recommended_action: str,
    evidence: list[str],
) -> Dict[str, Any]:

    # Only create incidents for meaningful threats
    if threat_score < 30:
        return {
            "incident_created": False,
            "reason": "Threat score below incident threshold.",
        }

    severity = determine_severity(threat_score)

    title = (
        "Critical Account Takeover Risk"
        if severity == "CRITICAL"
        else "Suspicious Account Security Activity"
    )

    description = (
        f"FinGuru detected a correlated security threat "
        f"with threat score {threat_score}. "
        f"Threat level: {threat_level}. "
        f"Recommended action: {recommended_action}."
    )

    if evidence:
        description += " Evidence: " + " ".join(evidence)

    incident = Incident(
        incident_type="SECURITY_THREAT",
        severity=severity,
        customer_id=customer_id,
        title=title,
        description=description,
        status="OPEN",
        recommended_action=recommended_action,
        detected_at=datetime.utcnow(),
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    # ---------------------------------------------------------
    # Evidence timeline
    # ---------------------------------------------------------

    evidence_timeline = []

    for index, item in enumerate(evidence, start=1):
        evidence_timeline.append({
            "sequence": index,
            "timestamp": datetime.utcnow().isoformat(),
            "evidence": item,
        })

    # ---------------------------------------------------------
    # Escalation decision
    # ---------------------------------------------------------

    human_escalation = severity in {
        "HIGH",
        "CRITICAL",
    }

    customer_verification_required = severity in {
        "MEDIUM",
        "HIGH",
        "CRITICAL",
    }

    return {
        "incident_created": True,
        "incident": {
            "id": incident.id,
            "incident_type": incident.incident_type,
            "severity": incident.severity,
            "customer_id": incident.customer_id,
            "title": incident.title,
            "description": incident.description,
            "status": incident.status,
            "recommended_action": incident.recommended_action,
            "detected_at": incident.detected_at,
        },
        "response_workflow": {
            "detection": True,
            "risk_score": threat_score,
            "incident_created": True,
            "evidence_timeline": evidence_timeline,
            "customer_verification_required": customer_verification_required,
            "human_escalation": human_escalation,
            "resolution": False,
            "audit_log": False,
        },
    }


def resolve_incident(
    db: Session,
    incident_id: int,
) -> Dict[str, Any]:

    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise ValueError(
            f"Incident {incident_id} not found."
        )

    incident.status = "RESOLVED"
    incident.resolved_at = datetime.utcnow()

    db.commit()
    db.refresh(incident)

    return {
        "incident_id": incident.id,
        "status": incident.status,
        "resolved_at": incident.resolved_at,
    }