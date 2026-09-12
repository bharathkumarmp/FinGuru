from typing import Dict, Any, List


from app.policy.consent import check_consent
from app.policy.affordability import check_affordability
from app.policy.bias_check import check_bias
from app.policy.confidence import check_confidence
from app.policy.human_escalation import check_human_escalation


class PolicyEngine:
    """
    Central Policy + Privacy Guardrail for FinGuru.

    Architecture:

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
        Final Policy Decision
            ↓
        Allowed FinGuru Action

    Important principle:

        ML decides numbers
        Agents reason
        Policy enforces
        LLM communicates
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

        requested = (
            requested_purpose
            .strip()
            .lower()
        )

        allowed = [
            purpose.strip().lower()
            for purpose in allowed_purposes
        ]

        if requested in allowed:
            return {
                "passed": True,
                "reason": (
                    "Requested purpose is permitted."
                ),
            }

        return {
            "passed": False,
            "reason": (
                "Requested purpose is not permitted."
            ),
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
    # DETERMINE POLICY ACTION
    # ========================================================

    def determine_action(
        self,
        consent_passed: bool,
        purpose_passed: bool,
        affordability_passed: bool,
        bias_passed: bool,
        confidence_passed: bool,
        compliance_passed: bool,
        human_escalation_required: bool,
        risk_score: float,
        critical: bool,
    ) -> str:
        """
        Convert individual policy checks into a
        FinGuru-level action.

        Possible actions:

            SAVE
            WAIT
            WARN
            APPLY
            SEEK_HELP
            NO_ACTION
        """

        # ----------------------------------------------------
        # Critical security / financial situation
        # ----------------------------------------------------

        if critical:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Human escalation
        # ----------------------------------------------------

        if human_escalation_required:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Consent failure
        # ----------------------------------------------------

        if not consent_passed:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Purpose violation
        # ----------------------------------------------------

        if not purpose_passed:
            return "NO_ACTION"

        # ----------------------------------------------------
        # Compliance failure
        # ----------------------------------------------------

        if not compliance_passed:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Bias failure
        # ----------------------------------------------------

        if not bias_passed:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Affordability failure
        # ----------------------------------------------------

        if not affordability_passed:
            return "WAIT"

        # ----------------------------------------------------
        # Confidence failure
        # ----------------------------------------------------

        if not confidence_passed:
            return "SEEK_HELP"

        # ----------------------------------------------------
        # Risk warning
        # ----------------------------------------------------

        if risk_score >= 75:
            return "WARN"

        # ----------------------------------------------------
        # Everything passed
        # ----------------------------------------------------

        return "APPLY"

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

        # ====================================================
        # 1. CONSENT
        # ====================================================

        consent = check_consent(
            consent_given
        )

        # ====================================================
        # 2. PURPOSE LIMITATION
        # ====================================================

        purpose = self.check_purpose(
            requested_purpose,
            allowed_purposes,
        )

        # ====================================================
        # 3. AFFORDABILITY
        # ====================================================

        affordability = check_affordability(
            affordability_score=affordability_score,
            projected_emi_ratio=projected_emi_ratio,
            monthly_surplus=monthly_surplus,
            maximum_emi_ratio=(
                self.maximum_emi_ratio
            ),
            minimum_affordability_score=(
                self.minimum_affordability_score
            ),
        )

        # ====================================================
        # 4. BIAS CHECK
        # ====================================================

        bias = check_bias(
            bias_score=bias_score,
            maximum_bias_score=(
                self.maximum_bias_score
            ),
        )

        # ====================================================
        # 5. CONFIDENCE CHECK
        # ====================================================

        confidence_result = check_confidence(
            confidence=confidence,
            minimum_confidence=(
                self.minimum_confidence
            ),
        )

        # ====================================================
        # 6. COMPLIANCE CHECK
        # ====================================================

        compliance = self.check_compliance(
            compliance_passed=compliance_passed,
            compliance_reason=compliance_reason,
        )

        # ====================================================
        # 7. HUMAN ESCALATION
        # ====================================================

        human_escalation = check_human_escalation(
            risk_score=risk_score,
            confidence=confidence,
            critical=critical,
            minimum_confidence=(
                self.minimum_confidence
            ),
        )

        # ====================================================
        # 8. POLICY PASS
        # ====================================================

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

        # ====================================================
        # 9. FINAL ACTION
        # ====================================================

        final_action = self.determine_action(
            consent_passed=consent["passed"],
            purpose_passed=purpose["passed"],
            affordability_passed=(
                affordability["passed"]
            ),
            bias_passed=bias["passed"],
            confidence_passed=(
                confidence_result["passed"]
            ),
            compliance_passed=(
                compliance["passed"]
            ),
            human_escalation_required=(
                human_escalation["required"]
            ),
            risk_score=risk_score,
            critical=critical,
        )

        # ====================================================
        # 10. FAILED CHECKS
        # ====================================================

        failed_checks = []

        checks = {
            "consent": consent,
            "purpose_limitation": purpose,
            "affordability": affordability,
            "bias": bias,
            "confidence": confidence_result,
            "compliance": compliance,
        }

        for name, result in checks.items():

            if not result["passed"]:
                failed_checks.append(name)

        # ====================================================
        # 11. RETURN COMPLETE DECISION
        # ====================================================

        return {

            "policy_passed": policy_passed,

            "final_action": final_action,

            "failed_checks": failed_checks,

            "checks": checks,

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

            "guardrail": {

                "enforced": True,

                "decision_layer": (
                    "Policy + Privacy Guardrail"
                ),

                "principle": (
                    "ML decides numbers; "
                    "agents reason; "
                    "policy enforces; "
                    "LLM communicates."
                ),
            },
        }


# ============================================================
# DEFAULT POLICY ENGINE
# ============================================================

policy_engine = PolicyEngine()