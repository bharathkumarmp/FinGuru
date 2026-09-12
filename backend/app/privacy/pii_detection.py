import re
from typing import Any, Dict


# ============================================================
# PII PATTERNS
# ============================================================

PII_PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "phone": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)"
    ),

    "aadhaar": re.compile(
        r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"
    ),

    "pan": re.compile(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    ),

    "account_number": re.compile(
        r"\b\d{9,18}\b"
    ),
}


# ============================================================
# DETECT PII
# ============================================================

def detect_pii(value: Any) -> Dict[str, Any]:
    """
    Detect common personally identifiable information
    in a string.
    """

    text = str(value)

    detected = {}

    for pii_type, pattern in PII_PATTERNS.items():

        matches = pattern.findall(text)

        if matches:
            detected[pii_type] = matches

    return {
        "contains_pii": bool(detected),
        "types": list(detected.keys()),
        "matches": detected,
    }


# ============================================================
# DETECT PII IN DICTIONARY
# ============================================================

def detect_pii_in_record(
    record: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Detect PII across all fields in a dictionary.
    """

    results = {}

    for field, value in record.items():

        if value is None:
            continue

        result = detect_pii(value)

        if result["contains_pii"]:
            results[field] = result

    return {
        "contains_pii": bool(results),
        "fields": results,
    }