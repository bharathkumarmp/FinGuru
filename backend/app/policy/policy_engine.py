from typing import Dict, Any, List

from app.policy.consent import check_consent
from app.policy.affordability import check_affordability
from app.policy.bias_check import check_bias
from app.policy.confidence import check_confidence
from app.policy.human_escalation import check_human_escalation


class PolicyEngine:
    """
    Central policy and privacy guardrail engine.

    Policy flow:

        Consent
           ↓
        Purpose Limitation
           ↓
        Affordability
           ↓
        Bias Check
           ↓
        Confidence
           ↓
        Compliance
           ↓
        Human Escalation
           ↓
        Final Action
    """

    def __init__(
        self,
        minimum_confidence: float = 0.70,
        maximum_emi_ratio: float = 0.50,
        minimum_affordability_score: float = 40.0,
        maximum_bias_score: float = 0.20,
    ):
        self.minimum_confidence = minimum_confidence
        self.maximum_emi_ratio = maximum_emi_ratio
        self.minimum_affordability_score = (
            minimum_affordability_score
        )
        self.maximum_bias_score = maximum_bias_score

    # ========================================================
    # PURPOSE LIMITATION
    # ========================================================

    def check_purpose(
        self,
        requested_purpose: str,
        allowed_purposes: List[str],
    ) -> Dict[str, Any]:

        requested = requested_purpose.strip().lower()

        allowed = [
            purpose.strip().lower()
            for purpose in allowed_purposes
        ]

        if requested in allowed:
            return {
                "passed": True,
                "reason": "Requested purpose is permitted.",
            }

        return {
            "passed": False,
            "reason": "Requested purpose is not permitted.",
        }

    # ========================================================
    # COMPLIANCE
    # ========================================================

    def check_compliance(
        self,
        compliance_passed: bool = True,
        compliance_reason: str = (
            "No compliance violation detected."
        ),
    ) -> Dict[str, Any]:

        return {
            "passed": compliance_passed,
            "reason": compliance_reason,
        }

    # ========================================================
    # COMPLETE POLICY EVALUATION
    # ========================================================

    def evaluate(
        self,
        consent_given: bool,
        requested_purpose: str,
        allowed_purposes: List[str],
        affordability_score: float,
        projected_emi_ratio: float,
        monthly_surplus: float,
        confidence: float,
        risk_score: float,
        bias_score: float = 0.0,
        compliance_passed: bool = True,
        compliance_reason: str = (
            "No compliance violation detected."
        ),
        critical: bool = False,
    ) -> Dict[str, Any]:

        # ----------------------------------------------------
        # Consent
        # ----------------------------------------------------

        consent = check_consent(
            consent_given
        )

        # ----------------------------------------------------
        # Purpose limitation
        # ----------------------------------------------------

        purpose = self.check_purpose(
            requested_purpose,
            allowed_purposes,
        )

        # ----------------------------------------------------
        # Affordability
        # ----------------------------------------------------

        affordability = check_affordability(
            affordability_score=affordability_score,
            projected_emi_ratio=projected_emi_ratio,
            monthly_surplus=monthly_surplus,
            maximum_emi_ratio=self.maximum_emi_ratio,
            minimum_affordability_score=(
                self.minimum_affordability_score
            ),
        )

        # ----------------------------------------------------
        # Bias
        # ----------------------------------------------------

        bias = check_bias(
            bias_score=bias_score,
            maximum_bias_score=self.maximum_bias_score,
        )

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        confidence_result = check_confidence(
            confidence=confidence,
            minimum_confidence=self.minimum_confidence,
        )

        # ----------------------------------------------------
        # Compliance
        # ----------------------------------------------------

        compliance = self.check_compliance(
            compliance_passed=compliance_passed,
            compliance_reason=compliance_reason,
        )

        # ----------------------------------------------------
        # Human escalation
        # ----------------------------------------------------

        human_escalation = check_human_escalation(
            risk_score=risk_score,
            confidence=confidence,
            critical=critical,
            minimum_confidence=self.minimum_confidence,
        )

        # ----------------------------------------------------
        # Determine policy result
        # ----------------------------------------------------

        policy_passed = all(
            [
                consent["passed"],
                purpose["passed"],
                affordability["passed"],
                bias["passed"],
                confidence_result["passed"],
                compliance["passed"],
            ]
        )

        # ----------------------------------------------------
        # Determine final action
        # ----------------------------------------------------

        if human_escalation["required"]:
            final_action = "SEEK_HELP"

        elif not consent["passed"]:
            final_action = "SEEK_HELP"

        elif not purpose["passed"]:
            final_action = "NO_ACTION"

        elif not affordability["passed"]:
            final_action = "WAIT"

        elif not bias["passed"]:
            final_action = "SEEK_HELP"

        elif not confidence_result["passed"]:
            final_action = "SEEK_HELP"

        elif not compliance["passed"]:
            final_action = "SEEK_HELP"

        else:
            final_action = "ALLOW"

        # ----------------------------------------------------
        # Return complete policy decision
        # ----------------------------------------------------

        return {
            "policy_passed": policy_passed,

            "final_action": final_action,

            "checks": {
                "consent": consent,
                "purpose_limitation": purpose,
                "affordability": affordability,
                "bias": bias,
                "confidence": confidence_result,
                "compliance": compliance,
            },

            "human_escalation": human_escalation,

            "policy_configuration": {
                "minimum_confidence": (
                    self.minimum_confidence
                ),
                "maximum_emi_ratio": (
                    self.maximum_emi_ratio
                ),
                "minimum_affordability_score": (
                    self.minimum_affordability_score
                ),
                "maximum_bias_score": (
                    self.maximum_bias_score
                ),
            },
        }


# ============================================================
# DEFAULT POLICY ENGINE
# ============================================================

policy_engine = PolicyEngine()