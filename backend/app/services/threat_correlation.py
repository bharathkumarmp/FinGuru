from typing import Dict, Any


def calculate_threat_score(
    fraud_score: float,
    ueba_score: float,
    identity_risk_score: float,
) -> float:
    """
    Combine multiple security intelligence signals
    into a unified threat score.
    """

    score = (
        fraud_score * 0.40
        + ueba_score * 0.30
        + identity_risk_score * 0.30
    )

    return round(min(max(score, 0), 100), 2)


def correlate_security_signals(
    fraud_score: float,
    ueba_score: float,
    identity_risk_score: float,
    fraud_risk_level: str = "LOW",
    ueba_risk_level: str = "LOW",
    identity_risk_level: str = "LOW",
) -> Dict[str, Any]:

    threat_score = calculate_threat_score(
        fraud_score=fraud_score,
        ueba_score=ueba_score,
        identity_risk_score=identity_risk_score,
    )

    # ---------------------------------------------------------
    # Correlation rules
    # ---------------------------------------------------------

    evidence = []

    if fraud_score >= 50:
        evidence.append(
            "Elevated fraud risk detected."
        )

    if ueba_score >= 50:
        evidence.append(
            "Customer behavior deviates significantly "
            "from historical behavior."
        )

    if identity_risk_score >= 50:
        evidence.append(
            "Identity or account-takeover risk is elevated."
        )

    # Strong multi-signal correlation
    high_signal_count = sum(
        [
            fraud_score >= 50,
            ueba_score >= 50,
            identity_risk_score >= 50,
        ]
    )

    critical_signal_count = sum(
        [
            fraud_score >= 75,
            ueba_score >= 75,
            identity_risk_score >= 75,
        ]
    )

    if critical_signal_count >= 2:
        threat_score = max(threat_score, 90)
        evidence.append(
            "Multiple critical security signals correlate "
            "to a potential account takeover."
        )

    elif high_signal_count >= 2:
        threat_score = max(threat_score, 70)
        evidence.append(
            "Multiple elevated security signals correlate "
            "to a coordinated security threat."
        )

    # ---------------------------------------------------------
    # Threat classification
    # ---------------------------------------------------------

    if threat_score >= 75:
        threat_level = "CRITICAL"
        recommended_action = "BLOCK_AND_ESCALATE"

    elif threat_score >= 50:
        threat_level = "HIGH"
        recommended_action = "STEP_UP_AUTHENTICATION"

    elif threat_score >= 30:
        threat_level = "MEDIUM"
        recommended_action = "REVIEW_TRANSACTION"

    else:
        threat_level = "LOW"
        recommended_action = "ALLOW"

    if not evidence:
        evidence.append(
            "No significant correlated security threat detected."
        )

    # ---------------------------------------------------------
    # Evidence timeline
    # ---------------------------------------------------------

    evidence_timeline = []

    if fraud_score > 0:
        evidence_timeline.append({
            "source": "FRAUD_DETECTION",
            "score": fraud_score,
            "risk_level": fraud_risk_level,
        })

    if ueba_score > 0:
        evidence_timeline.append({
            "source": "UEBA",
            "score": ueba_score,
            "risk_level": ueba_risk_level,
        })

    if identity_risk_score > 0:
        evidence_timeline.append({
            "source": "IDENTITY_RISK",
            "score": identity_risk_score,
            "risk_level": identity_risk_level,
        })

    return {
        "threat_score": round(threat_score, 2),
        "threat_level": threat_level,
        "recommended_action": recommended_action,
        "signal_scores": {
            "fraud_score": fraud_score,
            "ueba_score": ueba_score,
            "identity_risk_score": identity_risk_score,
        },
        "correlation": {
            "high_signal_count": high_signal_count,
            "critical_signal_count": critical_signal_count,
        },
        "evidence": evidence,
        "evidence_timeline": evidence_timeline,
    }