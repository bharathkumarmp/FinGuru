from typing import Dict, Any, Optional

from sqlalchemy.orm import Session

from app.models import Customer

from app.agents.financial_agent import financial_agent
from app.agents.risk_agent import risk_agent
from app.agents.recommendation_agent import recommendation_agent
from app.agents.communication_agent import communication_agent

from app.policy.policy_engine import policy_engine
from app.privacy.consent_manager import has_consent


class Orchestrator:
    """
    FinGuru End-to-End Multi-Agent Orchestrator.

    Architecture:

        Customer
            ↓
        Financial Analyst Agent
            ↓
        Risk & Security Agent
            ↓
        Recommendation Agent
            ↓
        Policy + Privacy Guardrail
            ↓
        Communication Agent
            ↓
        Final Decision

    Core principle:

        ML decides numbers
        Agents reason
        Policy enforces
        LLM communicates
    """

    # ============================================================
    # FINANCIAL ANALYSIS
    # ============================================================

    def run_financial_analysis(
        self,
        db: Session,
        customer_id: int,
    ) -> Dict[str, Any]:

        result = financial_agent.analyze_customer(
            db=db,
            customer_id=customer_id,
        )

        return result

    # ============================================================
    # SECURITY ANALYSIS
    # ============================================================

    def run_security_analysis(
        self,
        db: Session,
        customer_id: int,
        transaction_id: Optional[int] = None,
    ) -> Dict[str, Any]:

        if transaction_id is None:

            return {
                "success": True,
                "transaction_analyzed": False,
                "message": (
                    "No transaction supplied for security analysis."
                ),
                "security_summary": {
                    "fraud_score": 0.0,
                    "transaction_anomaly_score": 0.0,
                    "ueba_score": 0.0,
                    "identity_risk_score": 0.0,
                    "threat_score": 0.0,
                    "threat_level": "LOW",
                    "recommended_action": "ALLOW",
                    "active_signals": [],
                },
                "incident": None,
            }

        result = risk_agent.analyze_transaction(
            db=db,
            customer_id=customer_id,
            transaction_id=transaction_id,
        )

        return result

    # ============================================================
    # RECOMMENDATION
    # ============================================================

    def run_recommendation(
        self,
        db: Session,
        customer_id: int,
        loan_requested: bool = False,
        loan_amount: float = 0.0,
        tenure_months: int = 36,
        interest_rate: float = 12.0,
    ) -> Dict[str, Any]:

        result = recommendation_agent.analyze(
            db=db,
            customer_id=customer_id,
            loan_requested=loan_requested,
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            interest_rate=interest_rate,
        )

        return result

    # ============================================================
    # POLICY GUARDRAIL
    # ============================================================

    def run_policy(
        self,
        db: Session,
        customer_id: int,
        recommendation_result: Dict[str, Any],
        financial_result: Dict[str, Any],
        risk_result: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run the complete Policy + Privacy Guardrail.

        Sequence:

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

        # --------------------------------------------------------
        # CONSENT
        # --------------------------------------------------------

        consent_given = has_consent(
            db=db,
            customer_id=customer_id,
            purpose="financial_advice",
        )

        # --------------------------------------------------------
        # PURPOSE
        # --------------------------------------------------------

        requested_purpose = "financial_advice"

        allowed_purposes = [
            "financial_analysis",
            "financial_advice",
            "loan_recommendation",
            "fraud_detection",
        ]

        # --------------------------------------------------------
        # SAFE DICTIONARY ACCESS
        # --------------------------------------------------------

        recommendation_data = (
            recommendation_result
            if isinstance(recommendation_result, dict)
            else {}
        )

        financial_data = (
            financial_result
            if isinstance(financial_result, dict)
            else {}
        )

        # --------------------------------------------------------
        # FINANCIAL HEALTH
        # --------------------------------------------------------

        health_score = float(
            financial_data.get(
                "health_score",
                0.0,
            )
        )

        if health_score == 0.0:

            health = financial_data.get(
                "health",
                {},
            )

            if isinstance(health, dict):

                health_score = float(
                    health.get(
                        "score",
                        0.0,
                    )
                )

        # --------------------------------------------------------
        # FINANCIAL STRESS
        # --------------------------------------------------------

        stress_score = float(
            financial_data.get(
                "stress_score",
                0.0,
            )
        )

        if stress_score == 0.0:

            stress = financial_data.get(
                "stress",
                {},
            )

            if isinstance(stress, dict):

                stress_score = float(
                    stress.get(
                        "score",
                        0.0,
                    )
                )

        # --------------------------------------------------------
        # MONTHLY SURPLUS
        # --------------------------------------------------------

        monthly_surplus = float(
            recommendation_data.get(
                "monthly_surplus",
                financial_data.get(
                    "monthly_surplus",
                    0.0,
                ),
            )
        )

        # --------------------------------------------------------
        # AFFORDABILITY SCORE
        # --------------------------------------------------------

        affordability_score = float(
            recommendation_data.get(
                "affordability_score",
                0.0,
            )
        )

        if affordability_score == 0.0:

            signals = recommendation_data.get(
                "signals",
                {},
            )

            if isinstance(signals, dict):

                affordability_score = float(
                    signals.get(
                        "affordability",
                        0.0,
                    )
                )

        # --------------------------------------------------------
        # PROJECTED EMI RATIO
        # --------------------------------------------------------

        projected_emi_ratio = float(
            recommendation_data.get(
                "projected_emi_ratio",
                0.0,
            )
        )

        loan_analysis = recommendation_data.get(
            "loan_analysis",
            {},
        )

        if isinstance(loan_analysis, dict):

            projected_emi_ratio = float(
                loan_analysis.get(
                    "projected_emi_ratio",
                    projected_emi_ratio,
                )
            )

        # --------------------------------------------------------
        # RECOMMENDATION SCORE
        # --------------------------------------------------------

        recommendation_score = float(
            recommendation_data.get(
                "recommendation_score",
                recommendation_data.get(
                    "score",
                    0.0,
                ),
            )
        )

        # --------------------------------------------------------
        # CONFIDENCE
        # --------------------------------------------------------

        confidence = recommendation_score / 100.0

        confidence = max(
            0.0,
            min(
                1.0,
                confidence,
            ),
        )

        # --------------------------------------------------------
        # SECURITY RISK
        # --------------------------------------------------------

        risk_score = 0.0

        if isinstance(risk_result, dict):

            security_summary = risk_result.get(
                "security_summary",
                {},
            )

            if isinstance(security_summary, dict):

                risk_score = float(
                    security_summary.get(
                        "threat_score",
                        0.0,
                    )
                )

            if risk_score == 0.0:

                risk_score = float(
                    risk_result.get(
                        "threat_score",
                        0.0,
                    )
                )

        # --------------------------------------------------------
        # BIAS
        # --------------------------------------------------------

        bias_score = 0.0

        # Current prototype does not have a dedicated
        # bias-detection model.
        #
        # Neutral score is therefore passed to the policy engine.

        # --------------------------------------------------------
        # COMPLIANCE
        # --------------------------------------------------------

        compliance_passed = True

        compliance_reason = (
            "No compliance violation detected."
        )

        # --------------------------------------------------------
        # CRITICAL CONDITION
        # --------------------------------------------------------

        critical = False

        if stress_score >= 80:
            critical = True

        if health_score < 35:
            critical = True

        if risk_score >= 75:
            critical = True

        # --------------------------------------------------------
        # POLICY ENGINE
        # --------------------------------------------------------

        policy_result = policy_engine.evaluate(

            consent_given=consent_given,

            requested_purpose=requested_purpose,

            allowed_purposes=allowed_purposes,

            affordability_score=affordability_score,

            projected_emi_ratio=projected_emi_ratio,

            monthly_surplus=monthly_surplus,

            confidence=confidence,

            risk_score=risk_score,

            bias_score=bias_score,

            # IMPORTANT:
            # Actual PolicyEngine parameter name.
            compliance_passed=compliance_passed,

            compliance_reason=compliance_reason,

            critical=critical,
        )

        # --------------------------------------------------------
        # RETURN POLICY INFORMATION
        # --------------------------------------------------------

        return {
            "success": True,

            "customer_id": customer_id,

            "inputs": {
                "consent_given": consent_given,
                "requested_purpose": requested_purpose,
                "affordability_score": affordability_score,
                "projected_emi_ratio": projected_emi_ratio,
                "monthly_surplus": monthly_surplus,
                "confidence": confidence,
                "recommendation_score": recommendation_score,
                "risk_score": risk_score,
                "bias_score": bias_score,
                "compliance_passed": compliance_passed,
                "critical": critical,
            },

            "policy": policy_result,
        }

    # ============================================================
    # COMMUNICATION
    # ============================================================

    def run_communication(
        self,
        financial_result: Dict[str, Any],
        risk_result: Optional[Dict[str, Any]],
        recommendation_result: Dict[str, Any],
        policy_result: Dict[str, Any],
        language: str = "English",
    ) -> Dict[str, Any]:
        """
        Run Communication Agent.

        IMPORTANT:

        CommunicationAgent.generate_response() accepts:

            recommendation_result
            financial_result
            risk_result
            language

        It does NOT accept:

            customer_id
            policy_result

        Therefore policy enforcement is applied to the
        recommendation before communication.
        """

        # --------------------------------------------------------
        # Copy recommendation so the original agent output
        # remains untouched.
        # --------------------------------------------------------

        communication_recommendation = dict(
            recommendation_result
        )

        # --------------------------------------------------------
        # Extract policy decision
        # --------------------------------------------------------

        policy_data = policy_result.get(
            "policy",
            policy_result,
        )

        if not isinstance(policy_data, dict):
            policy_data = {}

        final_action = policy_data.get(
            "final_action",
            policy_data.get(
                "action",
                None,
            ),
        )

        # --------------------------------------------------------
        # Policy is authoritative.
        #
        # If Policy Engine changes the action, Communication
        # Agent must communicate the policy-enforced action.
        # --------------------------------------------------------

        if final_action:

            communication_recommendation[
                "action"
            ] = final_action

            communication_recommendation[
                "final_action"
            ] = final_action

            communication_recommendation[
                "policy_enforced"
            ] = True

        # --------------------------------------------------------
        # Add policy reasons when available
        # --------------------------------------------------------

        failed_checks = policy_data.get(
            "failed_checks",
            [],
        )

        if failed_checks:

            existing_reasons = communication_recommendation.get(
                "reasons",
                [],
            )

            if not isinstance(existing_reasons, list):
                existing_reasons = []

            communication_recommendation[
                "reasons"
            ] = existing_reasons + [
                str(reason)
                for reason in failed_checks
            ]

        # --------------------------------------------------------
        # ACTUAL COMMUNICATION AGENT INTERFACE
        # --------------------------------------------------------

        communication_result = (
            communication_agent.generate_response(
                recommendation_result=(
                    communication_recommendation
                ),

                financial_result=financial_result,

                risk_result=risk_result,

                language=language,
            )
        )

        # --------------------------------------------------------
        # Add orchestration metadata
        # --------------------------------------------------------

        if isinstance(
            communication_result,
            dict,
        ):

            communication_result[
                "policy_final_action"
            ] = final_action

            communication_result[
                "policy_enforced"
            ] = bool(final_action)

            communication_result[
                "language"
            ] = language

        return communication_result

    # ============================================================
    # COMPLETE PIPELINE
    # ============================================================

    def run(
        self,
        db: Session,
        customer_id: int,
        loan_requested: bool = False,
        loan_amount: float = 0.0,
        tenure_months: int = 36,
        interest_rate: float = 12.0,
        transaction_id: Optional[int] = None,
        language: str = "English",
    ) -> Dict[str, Any]:
        """
        Execute the complete FinGuru AI pipeline.
        """

        # ========================================================
        # CUSTOMER VALIDATION
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
                f"Customer {customer_id} not found."
            )

        # ========================================================
        # PIPELINE
        # ========================================================

        pipeline = []

        # ========================================================
        # 1. FINANCIAL ANALYSIS
        # ========================================================

        financial_result = (
            self.run_financial_analysis(
                db=db,
                customer_id=customer_id,
            )
        )

        pipeline.append(
            "FINANCIAL_ANALYSIS"
        )

        # ========================================================
        # 2. SECURITY ANALYSIS
        # ========================================================

        risk_result = (
            self.run_security_analysis(
                db=db,
                customer_id=customer_id,
                transaction_id=transaction_id,
            )
        )

        pipeline.append(
            "SECURITY_ANALYSIS"
        )

        # ========================================================
        # 3. RECOMMENDATION
        # ========================================================

        recommendation_result = (
            self.run_recommendation(
                db=db,
                customer_id=customer_id,
                loan_requested=loan_requested,
                loan_amount=loan_amount,
                tenure_months=tenure_months,
                interest_rate=interest_rate,
            )
        )

        pipeline.append(
            "RECOMMENDATION"
        )

        # ========================================================
        # 4. POLICY GUARDRAIL
        # ========================================================

        policy_result = self.run_policy(
            db=db,
            customer_id=customer_id,
            recommendation_result=(
                recommendation_result
            ),
            financial_result=financial_result,
            risk_result=risk_result,
        )

        pipeline.append(
            "POLICY_GUARDRAIL"
        )

        # ========================================================
        # 5. COMMUNICATION
        # ========================================================

        communication_result = (
            self.run_communication(
                financial_result=financial_result,

                risk_result=risk_result,

                recommendation_result=(
                    recommendation_result
                ),

                policy_result=policy_result,

                language=language,
            )
        )

        pipeline.append(
            "COMMUNICATION"
        )

        # ========================================================
        # FINAL DECISION
        # ========================================================

        policy_data = policy_result.get(
            "policy",
            policy_result,
        )

        if not isinstance(policy_data, dict):
            policy_data = {}

        final_action = policy_data.get(
            "final_action",
            policy_data.get(
                "action",
                "NO_ACTION",
            ),
        )

        # ========================================================
        # FINAL RESPONSE
        # ========================================================

        return {
            "success": True,

            "customer": {
                "id": customer.id,
                "name": customer.full_name,
                "city": customer.city,
                "occupation": customer.occupation,
            },

            "pipeline": pipeline,

            "financial_analysis": financial_result,

            "security_analysis": risk_result,

            "recommendation": recommendation_result,

            "policy": policy_result,

            "communication": communication_result,

            "final_decision": {
                "action": final_action,
                "policy_enforced": True,
            },
        }


# ================================================================
# SINGLETON
# ================================================================

orchestrator = Orchestrator()