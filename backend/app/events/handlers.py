from typing import Any, Dict


# ============================================================
# EVENT HANDLER
# ============================================================

def handle_event(
    event: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Main FinGuru event handler.

    Routes events to the appropriate
    financial/security processing pipeline.
    """

    event_type = event.get("event_type")
    customer_id = event.get("customer_id")
    data = event.get("data", {})

    result = {
        "event_id": event.get("event_id"),
        "event_type": event_type,
        "customer_id": customer_id,
        "handled": True,
        "action": "NO_ACTION",
        "message": "",
    }

    # ========================================================
    # FINANCIAL EVENTS
    # ========================================================

    if event_type == "SALARY_CREDITED":

        result["action"] = "UPDATE_FINANCIAL_STATE"

        result["message"] = (
            "Salary credited. Financial state should "
            "be recalculated."
        )

    elif event_type == "EMI_DUE":

        result["action"] = "EMI_REMINDER"

        result["message"] = (
            "EMI due event detected."
        )

    elif event_type == "EMI_MISSED":

        result["action"] = "RECALCULATE_STRESS"

        result["message"] = (
            "Missed EMI detected. Financial stress "
            "should be recalculated."
        )

    elif event_type == "SPENDING_SPIKE":

        result["action"] = "ANALYZE_SPENDING"

        result["message"] = (
            "Spending spike detected."
        )

    elif event_type == "BALANCE_DROP":

        result["action"] = "ANALYZE_BALANCE"

        result["message"] = (
            "Significant balance drop detected."
        )

    elif event_type == "LARGE_TRANSACTION":

        result["action"] = "ANALYZE_TRANSACTION"

        result["message"] = (
            "Large transaction detected."
        )

    # ========================================================
    # SECURITY EVENTS
    # ========================================================

    elif event_type == "NEW_DEVICE":

        result["action"] = "IDENTITY_RISK_ANALYSIS"

        result["message"] = (
            "Transaction from a new device detected."
        )

    elif event_type == "NEW_BENEFICIARY":

        result["action"] = "IDENTITY_RISK_ANALYSIS"

        result["message"] = (
            "New beneficiary detected."
        )

    elif event_type == "SUSPICIOUS_TRANSACTION":

        result["action"] = "FRAUD_ANALYSIS"

        result["message"] = (
            "Suspicious transaction detected."
        )

    elif event_type == "FRAUD_DETECTED":

        result["action"] = "SECURITY_RESPONSE"

        result["message"] = (
            "Fraud event detected. Security response "
            "should be initiated."
        )

    elif event_type == "IDENTITY_RISK":

        result["action"] = "SECURITY_RESPONSE"

        result["message"] = (
            "Identity risk detected."
        )

    elif event_type == "SECURITY_THREAT":

        result["action"] = "INCIDENT_RESPONSE"

        result["message"] = (
            "Security threat detected. Incident response "
            "should be initiated."
        )

    else:

        result["handled"] = False

        result["action"] = "UNKNOWN_EVENT"

        result["message"] = (
            f"Unknown event type: {event_type}"
        )

    return result