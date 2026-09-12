from typing import Any, Dict, List


# ============================================================
# POLICY GUARDRAIL ENGINE
# ============================================================

class PolicyGuardrail:

    def __init__(
        self,
        minimum_confidence: float = 0.70,
        maximum_emi_ratio: float = 0.50,
        minimum_affordability_score: float = 40.0,
    ):
        self.minimum_confidence = minimum_confidence
        self.maximum_emi_ratio = maximum_emi_ratio
        self.minimum_affordability_score = minimum_affordability_score

    # ========================================================
    # CONSENT CHECK
    # ========================================================

    def check_consent(
        self,
        consent_given: bool,
    ) -> Dict[str, Any]:

        if consent_given:
            return {
                "passed": True,
                "reason": "Customer consent is available.",
            }

        return {
            "passed": False,
            "reason": "Customer consent is required.",
        }

    # ========================================================
    # PURPOSE LIMITATION
    # ========================================================

    def check_purpose(
        self,
        requested_purpose: str,
        allowed_purposes: List[str],
    ) -> Dict[str, Any]:

        purpose = requested_purpose.strip().lower()

        allowed = [
            item.strip().lower()
            for item in allowed_purposes
        ]

        if purpose in allowed:
            return {
                "passed": True,
                "reason": "Requested purpose is permitted.",
            }

        return {
            "passed": False,
            "reason": "Requested purpose is not permitted.",
        }

    # ========================================================
    # AFFORDABILITY CHECK
    # ========================================================

    def check_affordability(
        self,
        affordability_score: float,
        projected_emi_ratio: float,
        monthly_surplus: float,
    ) -> Dict[str, Any]:

        failures = []

        if affordability_score < self.minimum_affordability_score:
            failures.append(
                "Affordability score is below the permitted threshold."
            )

        if projected_emi_ratio > self.maximum_emi_ratio:
            failures.append(
                "Projected EMI ratio exceeds the permitted threshold."
            )

        if monthly_surplus < 0:
            failures.append(
                "Projected monthly cash flow is negative."
            )

        if failures:
            return {
                "passed": False,
                "reasons": failures,
            }

        return {
            "passed": True,
            "reasons": [
                "Customer passes affordability checks."
            ],
        }

    # ========================================================
    # BIAS CHECK
    # ========================================================

    def check_bias(
        self,
        bias_score: float = 0.0,
        maximum_bias_score: float = 0.20,
    ) -> Dict[str, Any]:

        if bias_score > maximum_bias_score:
            return {
                "passed": False,
                "reason": (
                    "Recommendation failed the configured "
                    "bias threshold."
                ),
            }

        return {
            "passed": True,
            "reason": "Bias score is within the permitted threshold.",
        }

    # ========================================================
    # CONFIDENCE CHECK
    # ========================================================

    def check_confidence(
        self,
        confidence: float,
    ) -> Dict[str, Any]:

        if confidence < self.minimum_confidence:
            return {
                "passed": False,
                "reason": (
                    "Model confidence is below the "
                    "required threshold."
                ),
            }

        return {
            "passed": True,
            "reason": "Model confidence is sufficient.",
        }

    # ========================================================
    # COMPLIANCE CHECK
    # ========================================================

    def check_compliance(
        self,
        compliance_passed: bool = True,
        compliance_reason: str = "No compliance violation detected.",
    ) -> Dict[str, Any]:

        return {
            "passed": compliance_passed,
            "reason": compliance_reason,
        }

    # ========================================================
    # HUMAN ESCALATION
    # ========================================================

    def check_human_escalation(
        self,
        risk_score: float,
        confidence: float,
        critical: bool = False,
    ) -> Dict[str, Any]:

        reasons = []

        if critical:
            reasons.append(
                "Critical risk requires human review."
            )

        if risk_score >= 75:
            reasons.append(
                "Risk score is critically high."
            )

        if confidence < self.minimum_confidence:
            reasons.append(
                "Low model confidence requires human review."
            )

        if reasons:
            return {
                "required": True,
                "reasons": reasons,
            }

        return {
            "required": False,
            "reasons": [],
        }

    # ========================================================
    # COMPLETE GUARDRAIL EVALUATION
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
        # Run all checks
        # ----------------------------------------------------

        consent = self.check_consent(
            consent_given
        )

        purpose = self.check_purpose(
            requested_purpose,
            allowed_purposes,
        )

        affordability = self.check_affordability(
            affordability_score,
            projected_emi_ratio,
            monthly_surplus,
        )

        bias = self.check_bias(
            bias_score
        )

        confidence_check = self.check_confidence(
            confidence
        )

        compliance = self.check_compliance(
            compliance_passed,
            compliance_reason,
        )

        human_escalation = self.check_human_escalation(
            risk_score,
            confidence,
            critical,
        )

        # ----------------------------------------------------
        # Determine whether recommendation is allowed
        # ----------------------------------------------------

        all_passed = all(
            [
                consent["passed"],
                purpose["passed"],
                affordability["passed"],
                bias["passed"],
                confidence_check["passed"],
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

        elif not confidence_check["passed"]:
            final_action = "SEEK_HELP"

        elif not compliance["passed"]:
            final_action = "SEEK_HELP"

        else:
            final_action = "ALLOW"

        # ----------------------------------------------------
        # Return complete policy decision
        # ----------------------------------------------------

        return {
            "policy_passed": all_passed,

            "final_action": final_action,

            "checks": {
                "consent": consent,
                "purpose_limitation": purpose,
                "affordability": affordability,
                "bias": bias,
                "confidence": confidence_check,
                "compliance": compliance,
            },

            "human_escalation": human_escalation,

            "policy_configuration": {
                "minimum_confidence": self.minimum_confidence,
                "maximum_emi_ratio": self.maximum_emi_ratio,
                "minimum_affordability_score": (
                    self.minimum_affordability_score
                ),
            },
        }


# ============================================================
# DEFAULT GUARDRAIL INSTANCE
# ============================================================

policy_guardrail = PolicyGuardrail()