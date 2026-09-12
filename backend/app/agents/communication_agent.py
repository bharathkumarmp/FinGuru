from typing import Any, Optional


class CommunicationAgent:
    """
    FinGuru Communication Agent

    Responsibilities:
    - Convert structured AI decisions into customer-friendly language
    - Explain recommendations
    - Explain financial risk
    - Explain loan decisions
    - Support basic language adaptation
    - Prepare context for the Copilot / LLM layer

    Architecture:

        Financial Agent
              |
        Risk Agent
              |
     Recommendation Agent
              |
              v
     Communication Agent
              |
        +-----+-----+
        |           |
        v           v
     Customer    Copilot / LLM
     Response
    """

    name = "communication"

    # ============================================================
    # LANGUAGE SUPPORT
    # ============================================================

    SUPPORTED_LANGUAGES = {
        "english": "English",
        "hindi": "Hindi",
        "gujarati": "Gujarati",
    }

    # ============================================================
    # SAFE VALUE HELPERS
    # ============================================================

    @staticmethod
    def _get(
        data: Optional[dict[str, Any]],
        key: str,
        default: Any = None,
    ) -> Any:

        if not isinstance(data, dict):
            return default

        return data.get(key, default)

    @staticmethod
    def _money(value: Any) -> str:

        try:
            value = float(value)
            return f"₹{value:,.2f}"

        except (TypeError, ValueError):
            return "₹0.00"

    @staticmethod
    def _percent(value: Any) -> str:

        try:
            value = float(value)

            return f"{value * 100:.1f}%"

        except (TypeError, ValueError):
            return "0.0%"

    # ============================================================
    # ACTION EXPLANATION
    # ============================================================

    def explain_action(
        self,
        action: str,
        reasons: list[str],
    ) -> str:
        """
        Convert a Next Best Action into a customer-friendly
        explanation.
        """

        action = str(action).upper()

        action_messages = {

            "SAVE": (
                "The recommended next step is to focus on "
                "building savings and improving your financial buffer."
            ),

            "WAIT": (
                "The recommended next step is to wait before "
                "taking the proposed financial action."
            ),

            "WARN": (
                "There are important financial or security risks "
                "that should be reviewed before proceeding."
            ),

            "APPLY": (
                "Based on the available financial information, "
                "the proposed action appears potentially suitable."
            ),

            "SEEK_HELP": (
                "Your situation requires additional attention. "
                "It is better to review the situation with an "
                "appropriate financial or banking support team."
            ),

            "NO_ACTION": (
                "No immediate financial action is recommended."
            ),
        }

        explanation = action_messages.get(
            action,
            "The system recommends reviewing your financial situation "
            "before taking the next step.",
        )

        if reasons:

            explanation += " "

            explanation += (
                "This recommendation is based on: "
                + "; ".join(reasons[:5])
                + "."
            )

        return explanation

    # ============================================================
    # FINANCIAL SUMMARY
    # ============================================================

    def create_financial_summary(
        self,
        financial_state: dict[str, Any],
        health: dict[str, Any],
        stress: dict[str, Any],
    ) -> str:
        """
        Create a simple customer-facing financial summary.
        """

        income = self._money(
            self._get(
                financial_state,
                "monthly_income",
                0,
            )
        )

        spending = self._money(
            self._get(
                financial_state,
                "monthly_spending",
                0,
            )
        )

        surplus = self._money(
            self._get(
                financial_state,
                "monthly_surplus",
                0,
            )
        )

        health_score = self._get(
            health,
            "score",
            0,
        )

        health_level = self._get(
            health,
            "level",
            "UNKNOWN",
        )

        stress_score = self._get(
            stress,
            "score",
            0,
        )

        stress_level = self._get(
            stress,
            "level",
            "UNKNOWN",
        )

        return (
            f"Your estimated monthly income is {income}, "
            f"while monthly spending is {spending}. "
            f"Your current monthly surplus is {surplus}. "
            f"Your financial health score is {health_score}/100 "
            f"({health_level}), and your financial stress score is "
            f"{stress_score}/100 ({stress_level})."
        )

    # ============================================================
    # LOAN EXPLANATION
    # ============================================================

    def explain_loan(
        self,
        loan_analysis: Optional[dict[str, Any]],
    ) -> str:
        """
        Explain loan suitability using the numerical result
        calculated by the Loan Risk service.
        """

        if not loan_analysis:

            return (
                "No loan simulation was requested."
            )

        proposed_emi = self._money(
            self._get(
                loan_analysis,
                "proposed_emi",
                0,
            )
        )

        projected_ratio = self._get(
            loan_analysis,
            "projected_emi_ratio",
            0,
        )

        risk_score = self._get(
            loan_analysis,
            "risk_score",
            0,
        )

        risk_level = self._get(
            loan_analysis,
            "risk_level",
            "UNKNOWN",
        )

        suitability = self._get(
            loan_analysis,
            "suitability",
            "UNKNOWN",
        )

        reasons = self._get(
            loan_analysis,
            "reasons",
            [],
        )

        result = (
            f"The proposed loan would have an estimated EMI of "
            f"{proposed_emi}. "
            f"The projected EMI-to-income ratio is "
            f"{self._percent(projected_ratio)}. "
            f"The estimated loan risk score is {risk_score}/100 "
            f"({risk_level}). "
            f"Loan suitability is currently {suitability}."
        )

        if reasons:

            result += (
                " Main reasons: "
                + "; ".join(
                    str(reason)
                    for reason in reasons[:4]
                )
                + "."
            )

        return result

    # ============================================================
    # OFFER EXPLANATION
    # ============================================================

    def explain_offer(
        self,
        offer_result: Optional[dict[str, Any]],
    ) -> str:
        """
        Explain the next-best-offer result.
        """

        if not offer_result:

            return "No personalized offer is available."

        offer = self._get(
            offer_result,
            "offer",
            "NO_OFFER",
        )

        score = self._get(
            offer_result,
            "offer_score",
            0,
        )

        reason = self._get(
            offer_result,
            "reason",
            "",
        )

        if offer == "NO_OFFER":

            return (
                "No personalized financial offer is currently "
                "recommended."
            )

        return (
            f"The current next-best recommendation is "
            f"{offer} with a prioritization score of "
            f"{score}/100. {reason}"
        )

    # ============================================================
    # COMPLETE RESPONSE
    # ============================================================

    def generate_response(
        self,
        recommendation_result: dict[str, Any],
        financial_result: Optional[dict[str, Any]] = None,
        risk_result: Optional[dict[str, Any]] = None,
        language: str = "English",
    ) -> dict[str, Any]:
        """
        Generate a customer-facing response from agent results.

        This is deterministic fallback communication.
        Later, the same structured context can be passed to
        the LLM Copilot.
        """

        language_key = str(
            language
        ).lower()

        selected_language = (
            self.SUPPORTED_LANGUAGES.get(
                language_key,
                "English",
            )
        )

        # --------------------------------------------------------
        # Recommendation
        # --------------------------------------------------------

        next_action = recommendation_result.get(
            "next_best_action",
            {},
        )

        action = self._get(
            next_action,
            "action",
            "NO_ACTION",
        )

        reasons = self._get(
            next_action,
            "reasons",
            [],
        )

        recommendation_score = self._get(
            next_action,
            "score",
            0,
        )

        # --------------------------------------------------------
        # Financial State
        # --------------------------------------------------------

        if financial_result:

            financial_state = financial_result.get(
                "financial_state",
                {},
            )

            health = financial_result.get(
                "financial_health",
                {},
            )

            stress = financial_result.get(
                "financial_stress",
                {},
            )

        else:

            financial_state = recommendation_result.get(
                "financial_state",
                {},
            )

            health = recommendation_result.get(
                "financial_health",
                {},
            )

            stress = recommendation_result.get(
                "financial_stress",
                {},
            )

        # --------------------------------------------------------
        # Customer
        # --------------------------------------------------------

        customer = recommendation_result.get(
            "customer",
            {},
        )

        customer_name = self._get(
            customer,
            "name",
            "Customer",
        )

        # --------------------------------------------------------
        # Build response
        # --------------------------------------------------------

        financial_summary = (
            self.create_financial_summary(
                financial_state,
                health,
                stress,
            )
        )

        action_explanation = (
            self.explain_action(
                action,
                reasons,
            )
        )

        loan_explanation = self.explain_loan(
            recommendation_result.get(
                "loan_analysis"
            )
        )

        offer_explanation = self.explain_offer(
            recommendation_result.get(
                "next_best_offer"
            )
        )

        # --------------------------------------------------------
        # Security section
        # --------------------------------------------------------

        security_summary = None

        if risk_result:

            security = risk_result.get(
                "security_summary",
                {},
            )

            threat_score = self._get(
                security,
                "threat_score",
                0,
            )

            threat_level = self._get(
                security,
                "threat_level",
                "LOW",
            )

            security_action = self._get(
                security,
                "recommended_action",
                "ALLOW_TRANSACTION",
            )

            if threat_score >= 30:

                security_summary = (
                    f"A security review detected a threat score "
                    f"of {threat_score}/100 ({threat_level}). "
                    f"The recommended security response is "
                    f"{security_action}."
                )

            else:

                security_summary = (
                    "No significant security anomaly was detected "
                    "in the analyzed transaction."
                )

        # --------------------------------------------------------
        # Full customer response
        # --------------------------------------------------------

        response_lines = [

            f"Hello {customer_name}.",

            "",

            "Financial Summary:",

            financial_summary,

            "",

            "Recommended Next Step:",

            action_explanation,

            "",

            f"Recommendation confidence score: "
            f"{recommendation_score}/100",

            "",

            "Loan Analysis:",

            loan_explanation,

            "",

            "Personalized Guidance:",

            offer_explanation,

        ]

        if security_summary:

            response_lines.extend(
                [
                    "",
                    "Security Update:",
                    security_summary,
                ]
            )

        response_lines.extend(
            [
                "",
                "Language:",
                selected_language,
            ]
        )

        response_text = "\n".join(
            response_lines
        )

        return {

            "agent": self.name,

            "language": selected_language,

            "customer_id": self._get(
                customer,
                "id",
                None,
            ),

            "action": action,

            "response": response_text,

            "structured_context": {

                "customer": customer,

                "financial_state": financial_state,

                "financial_health": health,

                "financial_stress": stress,

                "recommendation": next_action,

                "loan_analysis": recommendation_result.get(
                    "loan_analysis"
                ),

                "offer": recommendation_result.get(
                    "next_best_offer"
                ),

                "security": (
                    risk_result
                    if risk_result
                    else None
                ),

            },

            "llm_ready": True,

        }


# ================================================================
# SINGLETON
# ================================================================

communication_agent = CommunicationAgent()