from datetime import datetime
from typing import Any, Dict


# ============================================================
# CONSENT MANAGER
# ============================================================

class ConsentManager:
    """
    Simple in-memory consent manager for the prototype.

    Production implementation should persist consent
    records in the database.
    """

    def __init__(self):
        self.consents: Dict[int, Dict[str, Any]] = {}

    # ========================================================
    # GRANT CONSENT
    # ========================================================

    def grant_consent(
        self,
        customer_id: int,
        purposes: list[str],
    ) -> Dict[str, Any]:

        self.consents[customer_id] = {
            "customer_id": customer_id,
            "granted": True,
            "purposes": purposes,
            "granted_at": datetime.utcnow().isoformat(),
        }

        return self.consents[customer_id]

    # ========================================================
    # REVOKE CONSENT
    # ========================================================

    def revoke_consent(
        self,
        customer_id: int,
    ) -> Dict[str, Any]:

        self.consents[customer_id] = {
            "customer_id": customer_id,
            "granted": False,
            "purposes": [],
            "revoked_at": datetime.utcnow().isoformat(),
        }

        return self.consents[customer_id]

    # ========================================================
    # CHECK CONSENT
    # ========================================================

    def has_consent(
        self,
        customer_id: int,
        purpose: str,
    ) -> bool:

        consent = self.consents.get(
            customer_id
        )

        if not consent:
            return False

        if not consent.get("granted"):
            return False

        return purpose in consent.get(
            "purposes",
            [],
        )

    # ========================================================
    # GET CONSENT
    # ========================================================

    def get_consent(
        self,
        customer_id: int,
    ) -> Dict[str, Any]:

        return self.consents.get(
            customer_id,
            {
                "customer_id": customer_id,
                "granted": False,
                "purposes": [],
            },
        )


# ============================================================
# GLOBAL CONSENT MANAGER
# ============================================================

consent_manager = ConsentManager()