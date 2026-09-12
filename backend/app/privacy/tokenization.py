import hashlib
import os
from typing import Any


# ============================================================
# TOKENIZATION SECRET
# ============================================================

TOKEN_SECRET = os.getenv(
    "FINGURU_TOKEN_SECRET",
    "finguru-development-secret",
)


# ============================================================
# TOKENIZE VALUE
# ============================================================

def tokenize(value: Any) -> str:
    """
    Generate a deterministic token for a sensitive value.

    The original value is never returned.
    """

    if value is None:
        return ""

    raw_value = str(value)

    payload = (
        TOKEN_SECRET
        + ":"
        + raw_value
    )

    digest = hashlib.sha256(
        payload.encode("utf-8")
    ).hexdigest()

    return f"TKN_{digest[:16].upper()}"


# ============================================================
# TOKENIZE RECORD
# ============================================================

def tokenize_record(
    record: dict,
    sensitive_fields: list[str],
) -> dict:
    """
    Replace sensitive fields with deterministic tokens.
    """

    result = dict(record)

    for field in sensitive_fields:

        if field in result and result[field] is not None:
            result[field] = tokenize(
                result[field]
            )

    return result