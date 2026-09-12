from typing import Any

from sqlalchemy.orm import Session

from app.models import Customer, Transaction

from app.services.fraud_detection import analyze_transaction
from app.services.transaction_anomaly import detect_transaction_anomaly
from app.services.ueba import analyze_customer_behavior
from app.services.identity_risk import analyze_identity_risk
from app.services.threat_correlation import correlate_security_signals
from app.services.incident_response import create_security_incident


class RiskSecurityAgent:
    """
    Risk & Security Agent.

    Combines:
        Fraud Detection
        Transaction Anomaly
        UEBA
        Identity Risk
              |
              v
        Threat Correlation
              |
              v
        Incident Response
    """

    name = "risk_security"

    # ============================================================
    # HELPER: READ VALUE FROM DICT OR SQLALCHEMY OBJECT
    # ============================================================

    @staticmethod
    def _get_value(
        result: Any,
        key: str,
        default: Any = None,
    ) -> Any:

        if result is None:
            return default

        if isinstance(result, dict):
            return result.get(key, default)

        return getattr(
            result,
            key,
            default,
        )

    # ============================================================
    # CONVERT RESULT TO DICT
    # ============================================================

    @staticmethod
    def _to_dict(result: Any) -> dict[str, Any]:

        if result is None:
            return {}

        if isinstance(result, dict):
            return result

        # SQLAlchemy model
        if hasattr(result, "__table__"):

            return {
                column.name: getattr(
                    result,
                    column.name,
                )
                for column in result.__table__.columns
            }

        # Generic Python object
        if hasattr(result, "__dict__"):

            return {
                key: value
                for key, value in vars(result).items()
                if not key.startswith("_")
            }

        return {}

    # ============================================================
    # TRANSACTION SECURITY ANALYSIS
    # ============================================================

    def analyze_transaction(
        self,
        db: Session,
        customer_id: int,
        transaction_id: int,
    ) -> dict[str, Any]:

        # --------------------------------------------------------
        # VERIFY CUSTOMER
        # --------------------------------------------------------

        customer = (
            db.query(Customer)
            .filter(
                Customer.id == customer_id
            )
            .first()
        )

        if not customer:
            raise ValueError(
                f"Customer {customer_id} not found"
            )

        # --------------------------------------------------------
        # VERIFY TRANSACTION
        # --------------------------------------------------------

        transaction = (
            db.query(Transaction)
            .filter(
                Transaction.id == transaction_id,
                Transaction.customer_id == customer_id,
            )
            .first()
        )

        if not transaction:
            raise ValueError(
                f"Transaction {transaction_id} not found "
                f"for customer {customer_id}"
            )

        # ========================================================
        # 1. FRAUD DETECTION
        # ========================================================

        fraud_raw = analyze_transaction(
            db=db,
            transaction_id=transaction_id,
        )

        fraud_result = self._to_dict(
            fraud_raw
        )

        # ========================================================
        # 2. TRANSACTION ANOMALY
        # ========================================================

        anomaly_raw = detect_transaction_anomaly(
            db=db,
            customer_id=customer_id,
            transaction_id=transaction_id,
        )

        anomaly_result = self._to_dict(
            anomaly_raw
        )

        # ========================================================
        # 3. UEBA
        # ========================================================

        ueba_raw = analyze_customer_behavior(
            db=db,
            customer_id=customer_id,
            transaction_id=transaction_id,
        )

        ueba_result = self._to_dict(
            ueba_raw
        )

        # ========================================================
        # 4. IDENTITY RISK
        # ========================================================

        identity_raw = analyze_identity_risk(
            db=db,
            customer_id=customer_id,
            transaction_id=transaction_id,
        )

        identity_result = self._to_dict(
            identity_raw
        )

        # ========================================================
        # 5. EXTRACT FRAUD SCORE
        # ========================================================

        fraud_score = float(
            self._get_value(
                fraud_raw,
                "fraud_score",
                0,
            )
            or 0
        )

        # ========================================================
        # 6. EXTRACT ANOMALY SCORE
        # ========================================================

        anomaly_score = float(
            self._get_value(
                anomaly_raw,
                "anomaly_score",
                0,
            )
            or 0
        )

        # ========================================================
        # 7. EXTRACT UEBA SCORE
        # ========================================================

        ueba_score = float(
            self._get_value(
                ueba_raw,
                "ueba_score",
                self._get_value(
                    ueba_raw,
                    "score",
                    0,
                ),
            )
            or 0
        )

        # ========================================================
        # 8. EXTRACT IDENTITY SCORE
        # ========================================================

        identity_score = float(
            self._get_value(
                identity_raw,
                "identity_risk_score",
                self._get_value(
                    identity_raw,
                    "risk_score",
                    0,
                ),
            )
            or 0
        )

        # ========================================================
        # 9. RISK LEVELS
        # ========================================================

        fraud_level = (
            self._get_value(
                fraud_raw,
                "risk_level",
                "LOW",
            )
            or "LOW"
        )

        ueba_level = (
            self._get_value(
                ueba_raw,
                "risk_level",
                self._get_value(
                    ueba_raw,
                    "ueba_level",
                    "LOW",
                ),
            )
            or "LOW"
        )

        identity_level = (
            self._get_value(
                identity_raw,
                "risk_level",
                self._get_value(
                    identity_raw,
                    "identity_risk_level",
                    "LOW",
                ),
            )
            or "LOW"
        )

        # ========================================================
        # 10. THREAT CORRELATION
        # ========================================================

        threat_result = correlate_security_signals(
            fraud_score=fraud_score,
            ueba_score=ueba_score,
            identity_risk_score=identity_score,
            fraud_risk_level=fraud_level,
            ueba_risk_level=ueba_level,
            identity_risk_level=identity_level,
        )

        threat_score = float(
            threat_result.get(
                "threat_score",
                0,
            )
            or 0
        )

        threat_level = (
            threat_result.get(
                "threat_level",
                "LOW",
            )
            or "LOW"
        )

        recommended_action = (
            threat_result.get(
                "recommended_action",
                "ALLOW_TRANSACTION",
            )
            or "ALLOW_TRANSACTION"
        )

        # ========================================================
        # 11. ACTIVE SIGNALS
        # ========================================================

        signals = {

            "fraud": fraud_score >= 50,

            "transaction_anomaly": (
                anomaly_score >= 30
            ),

            "ueba": (
                ueba_score >= 30
            ),

            "identity_risk": (
                identity_score >= 30
            ),

            "threat_correlation": (
                threat_score >= 30
            ),
        }

        active_signals = [
            name
            for name, active in signals.items()
            if active
        ]

        # ========================================================
        # 12. SECURITY ASSESSMENT
        # ========================================================

        if threat_level == "CRITICAL":

            assessment = (
                "Critical security risk detected. "
                "Multiple security signals indicate a "
                "potential account takeover or fraudulent "
                "transaction."
            )

        elif threat_level == "HIGH":

            assessment = (
                "High security risk detected. "
                "The transaction should undergo additional "
                "authentication or security review."
            )

        elif threat_level == "MEDIUM":

            assessment = (
                "Moderate security risk detected. "
                "The transaction contains unusual behavior "
                "and should be reviewed."
            )

        else:

            assessment = (
                "Transaction behavior appears consistent "
                "with the customer's observed baseline."
            )

        # ========================================================
        # 13. EVIDENCE
        # ========================================================

        evidence = threat_result.get(
            "evidence",
            [],
        )

        if not isinstance(evidence, list):
            evidence = []

        evidence = list(
            dict.fromkeys(evidence)
        )

        # ========================================================
        # 14. INCIDENT RESPONSE
        # ========================================================

        incident = None

        if threat_score >= 30:

            incident = create_security_incident(
                db=db,
                customer_id=customer_id,
                threat_score=threat_score,
                threat_level=threat_level,
                recommended_action=recommended_action,
                evidence=evidence,
            )

        # ========================================================
        # 15. FINAL RESULT
        # ========================================================

        return {

            "agent": self.name,

            "customer": {
                "id": customer.id,
                "name": customer.full_name,
            },

            "transaction": {
                "id": transaction.id,
                "amount": transaction.amount,
                "merchant": transaction.merchant,
                "category": transaction.category,
                "location": transaction.location,
                "device_id": transaction.device_id,
                "beneficiary": transaction.beneficiary,
            },

            "fraud": fraud_result,

            "transaction_anomaly": anomaly_result,

            "ueba": ueba_result,

            "identity_risk": identity_result,

            "threat_correlation": threat_result,

            "security_summary": {

                "fraud_score": fraud_score,

                "transaction_anomaly_score": (
                    anomaly_score
                ),

                "ueba_score": ueba_score,

                "identity_risk_score": (
                    identity_score
                ),

                "threat_score": threat_score,

                "threat_level": threat_level,

                "recommended_action": (
                    recommended_action
                ),

                "active_signals": active_signals,
            },

            "assessment": assessment,

            "incident": incident,
        }


# ================================================================
# SINGLETON
# ================================================================

risk_security_agent = RiskSecurityAgent()

risk_agent = risk_security_agent