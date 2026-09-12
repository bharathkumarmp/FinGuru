from typing import Any

from sqlalchemy.orm import Session

from app.models import (
    Customer,
    CustomerFeatures,
    FinancialHealth,
    FinancialStress,
)

from app.services.recommendation_engine import generate_recommendation
from app.services.loan_risk import calculate_loan_risk
from app.services.offer_engine import generate_next_best_offer
from app.services.life_events import detect_life_events


class RecommendationAgent:
    """
    FinGuru Recommendation Agent

    Responsibilities:
    - Analyze customer's financial state
    - Evaluate loan suitability
    - Generate Next Best Action
    - Generate personalized offers
    - Consider financial health and stress
    - Consider detected life events

    Architecture:

        Financial Intelligence
                |
                v
        Recommendation Agent
                |
                v
          Policy Engine
                |
                v
          Final Action

    The Recommendation Agent proposes an action.
    The Policy Engine remains the final authority.
    """

    name = "recommendation"

    # ============================================================
    # HELPER: SAFE FLOAT CONVERSION
    # ============================================================

    @staticmethod
    def _to_float(
        value: Any,
        default: float = 0.0,
    ) -> float:

        try:

            if value is None:
                return default

            return float(value)

        except (TypeError, ValueError):

            return default

    # ============================================================
    # HELPER: SAFE VALUE EXTRACTION
    # ============================================================

    @staticmethod
    def _get_value(
        obj: Any,
        *names: str,
        default: Any = None,
    ) -> Any:

        if obj is None:
            return default

        for name in names:

            if isinstance(obj, dict):

                if name in obj:
                    return obj[name]

            elif hasattr(obj, name):

                value = getattr(obj, name)

                if value is not None:
                    return value

        return default

    # ============================================================
    # HELPER: NORMALIZE LIFE EVENTS
    # ============================================================

    @staticmethod
    def _normalize_life_events(
        events: Any,
    ) -> list[dict[str, Any]]:
        """
        Convert life-event results into a standard format.
        """

        if not events:
            return []

        # Dictionary containing a list of events
        if isinstance(events, dict):

            if "events" in events:

                events = events["events"]

            elif (
                "event_type" in events
                or "type" in events
            ):

                events = [events]

            else:

                events = [events]

        normalized = []

        for event in events:

            if isinstance(event, dict):

                event_type = event.get(
                    "event_type",
                    event.get(
                        "type",
                        "UNKNOWN",
                    ),
                )

                confidence = event.get(
                    "confidence",
                    0.0,
                )

                reason = event.get(
                    "reason",
                    "",
                )

            else:

                event_type = str(event)

                confidence = 0.0

                reason = ""

            normalized.append(
                {
                    "event_type": str(
                        event_type
                    ),

                    "confidence": (
                        RecommendationAgent._to_float(
                            confidence
                        )
                    ),

                    "reason": str(
                        reason
                    ),
                }
            )

        return normalized

    # ============================================================
    # MAIN ANALYSIS
    # ============================================================

    def analyze(
        self,
        db: Session,
        customer_id: int,
        loan_requested: bool = False,
        loan_amount: float = 0.0,
        tenure_months: int = 36,
        interest_rate: float = 12.0,
    ) -> dict[str, Any]:

        # ========================================================
        # 1. FIND CUSTOMER
        # ========================================================

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

        # ========================================================
        # 2. FIND CUSTOMER FEATURES
        # ========================================================

        features = (
            db.query(CustomerFeatures)
            .filter(
                CustomerFeatures.customer_id
                == customer_id
            )
            .first()
        )

        if not features:

            raise ValueError(
                f"Financial features not found "
                f"for customer {customer_id}"
            )

        # ========================================================
        # 3. GET LATEST FINANCIAL HEALTH
        # ========================================================

        health = (
            db.query(FinancialHealth)
            .filter(
                FinancialHealth.customer_id
                == customer_id
            )
            .order_by(
                FinancialHealth.calculated_at.desc()
            )
            .first()
        )

        # ========================================================
        # 4. GET LATEST FINANCIAL STRESS
        # ========================================================

        stress = (
            db.query(FinancialStress)
            .filter(
                FinancialStress.customer_id
                == customer_id
            )
            .order_by(
                FinancialStress.calculated_at.desc()
            )
            .first()
        )

        # ========================================================
        # 5. EXTRACT FINANCIAL FEATURES
        # ========================================================

        monthly_income = self._to_float(
            getattr(
                features,
                "avg_monthly_income",
                0.0,
            )
        )

        monthly_spending = self._to_float(
            getattr(
                features,
                "avg_monthly_spending",
                0.0,
            )
        )

        monthly_surplus = (
            monthly_income
            - monthly_spending
        )

        savings_rate = self._to_float(
            getattr(
                features,
                "savings_rate",
                0.0,
            )
        )

        emi_ratio = self._to_float(
            getattr(
                features,
                "emi_ratio",
                0.0,
            )
        )

        income_stability = self._to_float(
            getattr(
                features,
                "income_stability",
                0.0,
            )
        )

        cash_buffer = self._to_float(
            getattr(
                features,
                "cash_buffer",
                0.0,
            )
        )

        # ========================================================
        # 6. HEALTH SCORE
        # ========================================================

        health_score = self._to_float(
            self._get_value(
                health,
                "score",
                default=0.0,
            )
        )

        health_level = self._get_value(
            health,
            "health_level",
            "level",
            default="UNKNOWN",
        )

        # ========================================================
        # 7. STRESS SCORE
        # ========================================================

        stress_score = self._to_float(
            self._get_value(
                stress,
                "stress_score",
                "score",
                default=0.0,
            )
        )

        stress_level = self._get_value(
            stress,
            "stress_level",
            "level",
            default="UNKNOWN",
        )

        # ========================================================
        # 8. DETECT LIFE EVENTS
        # ========================================================

        detected_events = detect_life_events(
            db=db,
            customer_id=customer_id,
        )

        life_events = (
            self._normalize_life_events(
                detected_events
            )
        )

        # ========================================================
        # 9. LOAN ANALYSIS
        # ========================================================

        loan_analysis = None

        loan_suitable = True

        projected_emi_ratio = emi_ratio

        if loan_requested:

            if loan_amount <= 0:

                raise ValueError(
                    "loan_amount must be greater than zero "
                    "when loan_requested=True"
                )

            loan_analysis = calculate_loan_risk(
                features,
                loan_amount,
                tenure_months,
                interest_rate,
            )

            # ----------------------------------------------------
            # Extract suitability
            # ----------------------------------------------------

            suitability = self._get_value(
                loan_analysis,
                "suitability",
                "loan_suitability",
                "status",
                default="NOT_SUITABLE",
            )

            suitability = str(
                suitability
            ).upper()

            loan_suitable = (
                suitability == "SUITABLE"
            )

            # ----------------------------------------------------
            # Extract projected EMI ratio
            # ----------------------------------------------------

            projected_emi_ratio = self._to_float(
                self._get_value(
                    loan_analysis,
                    "projected_emi_ratio",
                    "emi_ratio",
                    default=emi_ratio,
                ),
                default=emi_ratio,
            )

        # ========================================================
        # 10. RECOMMENDATION ENGINE
        # ========================================================
        #
        # EXACT CURRENT SIGNATURE:
        #
        # generate_recommendation(
        #     health_score,
        #     stress_score,
        #     monthly_income,
        #     monthly_surplus,
        #     projected_emi_ratio,
        #     loan_suitable,
        #     fraud_risk,
        #     customer_preference,
        #     loan_requested
        # )
        # ========================================================

        recommendation = generate_recommendation(
            health_score=health_score,
            stress_score=stress_score,
            monthly_income=monthly_income,
            monthly_surplus=monthly_surplus,
            projected_emi_ratio=projected_emi_ratio,
            loan_suitable=loan_suitable,
            fraud_risk=0.0,
            customer_preference=50.0,
            loan_requested=loan_requested,
        )

        # ========================================================
        # 11. EXTRACT ACTION
        # ========================================================

        action = self._get_value(
            recommendation,
            "action",
            "recommendation",
            "next_best_action",
            "final_action",
            default="NO_ACTION",
        )

        # ========================================================
        # 12. EXTRACT SCORE
        # ========================================================

        recommendation_score = self._to_float(
            self._get_value(
                recommendation,
                "recommendation_score",
                "score",
                default=0.0,
            )
        )

        # ========================================================
        # 13. EXTRACT REASONS
        # ========================================================

        reasons = self._get_value(
            recommendation,
            "reasons",
            "reason",
            default=[],
        )

        if reasons is None:

            reasons = []

        elif isinstance(
            reasons,
            str,
        ):

            reasons = [reasons]

        elif isinstance(
            reasons,
            (list, tuple),
        ):

            reasons = [
                str(reason)
                for reason in reasons
            ]

        else:

            reasons = [
                str(reasons)
            ]

        # ========================================================
        # 14. EXTRACT SIGNALS
        # ========================================================

        signals = self._get_value(
            recommendation,
            "signals",
            default={},
        )

        if not isinstance(
            signals,
            dict,
        ):

            signals = {}

        # ========================================================
        # 15. ADD AGENT REASONING
        # ========================================================

        if monthly_surplus < 0:

            reasons.append(
                "Monthly cash flow is negative; "
                "financial stabilization should be prioritized."
            )

        if stress_score >= 60:

            reasons.append(
                "Financial stress is elevated; "
                "new financial obligations should be approached cautiously."
            )

        if health_score < 50:

            reasons.append(
                "Financial health is below the preferred range."
            )

        if loan_requested and not loan_suitable:

            reasons.append(
                "The requested loan is currently not suitable "
                "based on affordability and financial risk."
            )

        # Remove duplicate reasons

        reasons = list(
            dict.fromkeys(reasons)
        )

        # ========================================================
        # 16. PERSONALIZED OFFER ENGINE
        # ========================================================
        #
        # EXACT CURRENT SIGNATURE:
        #
        # generate_next_best_offer(
        #     health_score,
        #     stress_score,
        #     monthly_surplus,
        #     savings_rate,
        #     emi_ratio,
        #     income_stability,
        #     consent_given,
        #     life_events
        # )
        #
        # Notice:
        # monthly_income and monthly_spending are NOT passed.
        # ========================================================

        offer_result = generate_next_best_offer(
            health_score=health_score,
            stress_score=stress_score,
            monthly_surplus=monthly_surplus,
            savings_rate=savings_rate,
            emi_ratio=emi_ratio,
            income_stability=income_stability,
            consent_given=True,
            life_events=life_events,
        )

        # ========================================================
        # 17. STRATEGIC PRIORITY
        # ========================================================

        if monthly_surplus < 0:

            priority = "financial_stabilization"

        elif stress_score >= 60:

            priority = "stress_reduction"

        elif health_score >= 65:

            priority = "financial_growth"

        else:

            priority = "financial_improvement"

        # ========================================================
        # 18. RISK SENSITIVITY
        # ========================================================

        risk_sensitive = (
            monthly_surplus < 0
            or stress_score >= 60
            or health_score < 50
        )

        # ========================================================
        # 19. FINAL RESULT
        # ========================================================

        return {

            "agent": self.name,

            "customer": {

                "id": customer.id,

                "name": customer.full_name,

                "city": customer.city,

                "occupation": customer.occupation,

            },

            "financial_state": {

                "monthly_income": round(
                    monthly_income,
                    2,
                ),

                "monthly_spending": round(
                    monthly_spending,
                    2,
                ),

                "monthly_surplus": round(
                    monthly_surplus,
                    2,
                ),

                "savings_rate": round(
                    savings_rate,
                    4,
                ),

                "emi_ratio": round(
                    emi_ratio,
                    4,
                ),

                "projected_emi_ratio": round(
                    projected_emi_ratio,
                    4,
                ),

                "income_stability": round(
                    income_stability,
                    4,
                ),

                "cash_buffer": round(
                    cash_buffer,
                    2,
                ),

            },

            "financial_health": {

                "score": round(
                    health_score,
                    2,
                ),

                "level": health_level,

            },

            "financial_stress": {

                "score": round(
                    stress_score,
                    2,
                ),

                "level": stress_level,

            },

            "life_events": life_events,

            "loan_analysis": loan_analysis,

            "next_best_action": {

                "action": str(action),

                "score": round(
                    recommendation_score,
                    2,
                ),

                "reasons": reasons,

                "signals": signals,

            },

            "next_best_offer": offer_result,

            "agent_reasoning": {

                "priority": priority,

                "loan_requested": loan_requested,

                "loan_suitable": loan_suitable,

                "risk_sensitive": risk_sensitive,

                "decision_basis": [

                    "financial_health",

                    "financial_stress",

                    "cash_flow",

                    "affordability",

                    "loan_suitability",

                    "life_events",

                ],

            },

        }


# ================================================================
# SINGLETON INSTANCE
# ================================================================

recommendation_agent = RecommendationAgent()