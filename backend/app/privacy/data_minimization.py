from typing import Any, Dict, List


# ============================================================
# MINIMIZE RECORD
# ============================================================

def minimize_record(
    record: Dict[str, Any],
    required_fields: List[str],
) -> Dict[str, Any]:
    """
    Return only fields required for the specified
    processing purpose.
    """

    return {
        field: record[field]
        for field in required_fields
        if field in record
    }


# ============================================================
# REMOVE EMPTY VALUES
# ============================================================

def remove_empty_values(
    record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Remove None and empty-string values.
    """

    return {
        key: value
        for key, value in record.items()
        if value is not None
        and value != ""
    }


# ============================================================
# MINIMIZE CUSTOMER DATA
# ============================================================

def minimize_customer_data(
    customer: Dict[str, Any],
    purpose: str,
) -> Dict[str, Any]:
    """
    Apply purpose-based data minimization.
    """

    purpose_fields = {

        "financial_analysis": [
            "customer_id",
            "monthly_income",
            "monthly_spending",
            "occupation",
            "city",
        ],

        "loan_recommendation": [
            "customer_id",
            "monthly_income",
            "monthly_spending",
            "existing_emi",
            "credit_utilization",
            "missed_emi_count",
            "savings_rate",
        ],

        "fraud_detection": [
            "customer_id",
            "transaction_id",
            "amount",
            "location",
            "device_id",
            "beneficiary",
            "timestamp",
        ],

        "financial_advice": [
            "customer_id",
            "monthly_income",
            "monthly_spending",
            "savings_rate",
            "emi_ratio",
            "financial_health",
            "financial_stress",
        ],
    }

    required_fields = purpose_fields.get(
        purpose,
        ["customer_id"],
    )

    return minimize_record(
        customer,
        required_fields,
    )