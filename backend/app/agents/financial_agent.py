from typing import Any

from sqlalchemy.orm import Session

from app.models import Customer, CustomerFeatures, FinancialHealth, FinancialStress
from app.services.customer_360 import get_customer_360
from app.services.life_events import detect_life_events
from app.services.digital_twin import simulate_financial_future


class FinancialAnalystAgent:
    """
    Financial Analyst Agent

    Responsibility:
    - Understand the customer's financial state
    - Summarize income, spending, savings and debt
    - Analyze financial health and stress
    - Detect relevant life events
    - Run digital-twin simulations when requested
    - Produce structured financial reasoning for downstream agents

    Principle:
    ML/services calculate the numbers.
    This agent interprets those numbers.
    """

    name = "financial_analyst"

    def analyze_customer(
        self,
        db: Session,
        customer_id: int,
    ) -> dict[str, Any]:

        customer = (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

        if not customer:
            raise ValueError(f"Customer {customer_id} not found")

        # ---------------------------------------------------------
        # CUSTOMER 360
        # ---------------------------------------------------------

        customer_360 = get_customer_360(
            db=db,
            customer_id=customer_id,
        )

        # ---------------------------------------------------------
        # FINANCIAL FEATURES
        # ---------------------------------------------------------

        features = (
            db.query(CustomerFeatures)
            .filter(CustomerFeatures.customer_id == customer_id)
            .first()
        )

        # ---------------------------------------------------------
        # LATEST FINANCIAL HEALTH
        # ---------------------------------------------------------

        health = (
            db.query(FinancialHealth)
            .filter(FinancialHealth.customer_id == customer_id)
            .order_by(FinancialHealth.calculated_at.desc())
            .first()
        )

        # ---------------------------------------------------------
        # LATEST FINANCIAL STRESS
        # ---------------------------------------------------------

        stress = (
            db.query(FinancialStress)
            .filter(FinancialStress.customer_id == customer_id)
            .order_by(FinancialStress.calculated_at.desc())
            .first()
        )

        # ---------------------------------------------------------
        # LIFE EVENTS
        # ---------------------------------------------------------

        life_events = detect_life_events(
            db=db,
            customer_id=customer_id,
        )

        # ---------------------------------------------------------
        # FINANCIAL STATE
        # ---------------------------------------------------------

        monthly_income = (
            features.avg_monthly_income
            if features
            else float(customer.monthly_income or 0)
        )

        monthly_spending = (
            features.avg_monthly_spending
            if features
            else 0.0
        )

        monthly_surplus = (
            monthly_income - monthly_spending
        )

        savings_rate = (
            features.savings_rate
            if features
            else 0.0
        )

        emi_ratio = (
            features.emi_ratio
            if features
            else 0.0
        )

        income_stability = (
            features.income_stability
            if features
            else 0.0
        )

        cash_buffer = (
            features.cash_buffer
            if features
            else 0.0
        )

        # ---------------------------------------------------------
        # HEALTH
        # ---------------------------------------------------------

        health_score = 0.0

        if health:
            health_score = float(
                getattr(health, "score", 0.0) or 0.0
            )

        health_level = (
            getattr(health, "health_level", "UNKNOWN")
            if health
            else "UNKNOWN"
        )

        # ---------------------------------------------------------
        # STRESS
        # ---------------------------------------------------------

        stress_score = 0.0

        if stress:
            stress_score = float(
                getattr(
                    stress,
                    "stress_score",
                    getattr(stress, "score", 0.0),
                )
                or 0.0
            )

        stress_level = (
            getattr(
                stress,
                "stress_level",
                getattr(stress, "level", "UNKNOWN"),
            )
            if stress
            else "UNKNOWN"
        )

        # ---------------------------------------------------------
        # FINANCIAL INTERPRETATION
        # ---------------------------------------------------------

        strengths = []
        concerns = []

        if savings_rate > 0.20:
            strengths.append("Healthy savings behavior")

        if income_stability >= 0.70:
            strengths.append("Stable income")

        if emi_ratio < 0.30:
            strengths.append("Manageable EMI burden")

        if monthly_surplus < 0:
            concerns.append("Monthly cash flow is negative")

        if emi_ratio >= 0.40:
            concerns.append("EMI burden is relatively high")

        if stress_score >= 60:
            concerns.append("Financial stress is elevated")

        if health_score < 50:
            concerns.append("Financial health requires improvement")

        if cash_buffer <= 0:
            concerns.append("Limited cash buffer")

        # ---------------------------------------------------------
        # AGENT SUMMARY
        # ---------------------------------------------------------

        if monthly_surplus < 0:
            overall_assessment = (
                "Customer currently has negative monthly cash flow "
                "and should prioritize financial stabilization."
            )

        elif stress_score >= 60:
            overall_assessment = (
                "Customer has positive cash flow but elevated "
                "financial stress and should avoid unnecessary "
                "financial commitments."
            )

        elif health_score >= 65:
            overall_assessment = (
                "Customer appears financially stable and may be "
                "able to consider suitable financial actions."
            )

        else:
            overall_assessment = (
                "Customer has a moderate financial position and "
                "should evaluate affordability before taking action."
            )

        return {
            "agent": self.name,
            "customer": {
                "id": customer.id,
                "name": customer.full_name,
                "city": customer.city,
                "occupation": customer.occupation,
            },
            "financial_state": {
                "monthly_income": round(monthly_income, 2),
                "monthly_spending": round(monthly_spending, 2),
                "monthly_surplus": round(monthly_surplus, 2),
                "savings_rate": round(savings_rate, 4),
                "emi_ratio": round(emi_ratio, 4),
                "income_stability": round(income_stability, 4),
                "cash_buffer": round(cash_buffer, 2),
            },
            "financial_health": {
                "score": health_score,
                "level": health_level,
            },
            "financial_stress": {
                "score": stress_score,
                "level": stress_level,
            },
            "life_events": life_events,
            "strengths": strengths,
            "concerns": concerns,
            "overall_assessment": overall_assessment,
            "customer_360": customer_360,
        }

    def simulate_loan(
        self,
        db: Session,
        customer_id: int,
        loan_amount: float,
        tenure_months: int,
        interest_rate: float,
    ) -> dict[str, Any]:
        """
        Run a financial digital-twin simulation.

        The digital-twin service performs the numerical simulation.
        The agent interprets the result.
        """

        simulation = simulate_financial_future(
            db=db,
            customer_id=customer_id,
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            interest_rate=interest_rate,
        )

        projected_health = simulation.get(
            "projected_health",
            simulation.get("health_score", 0),
        )

        projected_stress = simulation.get(
            "projected_stress",
            simulation.get("stress_score", 0),
        )

        recommendation = simulation.get(
            "recommendation",
            "WAIT",
        )

        if projected_health < 50:
            interpretation = (
                "The simulated loan materially weakens the "
                "customer's financial position."
            )

        elif projected_stress >= 60:
            interpretation = (
                "The simulated loan increases financial stress "
                "to a concerning level."
            )

        elif recommendation == "APPLY":
            interpretation = (
                "The simulated loan appears financially manageable "
                "under the supplied assumptions."
            )

        else:
            interpretation = (
                "The simulated loan requires caution before proceeding."
            )

        return {
            "agent": self.name,
            "customer_id": customer_id,
            "simulation": simulation,
            "interpretation": interpretation,
            "recommended_direction": recommendation,
        }


financial_agent = FinancialAnalystAgent()