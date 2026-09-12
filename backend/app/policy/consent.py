from typing import Dict, Any


def check_consent(
    consent_given: bool,
) -> Dict[str, Any]:
    """
    Check whether customer consent is available.
    """

    if consent_given:
        return {
            "passed": True,
            "reason": "Customer consent is available.",
        }

    return {
        "passed": False,
        "reason": "Customer consent is required.",
    }