from app.database import SessionLocal

from app.agents.orchestrator import orchestrator


def main():

    db = SessionLocal()

    try:

        print("=" * 70)
        print("FINGURU ORCHESTRATOR END-TO-END TEST")
        print("=" * 70)

        # ========================================================
        # COMPLETE FINANCIAL JOURNEY
        # ========================================================

        result = orchestrator.run(

            db=db,

            customer_id=1,

            loan_requested=True,

            loan_amount=300000,

            tenure_months=36,

            interest_rate=12,

            # No transaction for this first test.
            transaction_id=None,

            language="English",
        )

        # ========================================================
        # PIPELINE
        # ========================================================

        print("\nPIPELINE")
        print("-" * 70)

        for step in result["pipeline"]:
            print(f"✓ {step}")

        # ========================================================
        # FINANCIAL
        # ========================================================

        print("\nFINANCIAL ANALYSIS")
        print("-" * 70)

        financial = result["financial_analysis"]

        print(financial)

        # ========================================================
        # RECOMMENDATION
        # ========================================================

        print("\nRECOMMENDATION")
        print("-" * 70)

        recommendation = result["recommendation"]

        print(
            "Next Best Action:",
            recommendation.get(
                "next_best_action"
            ),
        )

        print(
            "Loan Analysis:",
            recommendation.get(
                "loan_analysis"
            ),
        )

        print(
            "Next Best Offer:",
            recommendation.get(
                "next_best_offer"
            ),
        )

        # ========================================================
        # POLICY
        # ========================================================

        print("\nPOLICY ENGINE")
        print("-" * 70)

        policy = result["policy"]

        print(
            "Original Action:",
            policy.get(
                "original_action"
            ),
        )

        print(
            "Final Action:",
            policy.get(
                "final_action"
            ),
        )

        print(
            "Consent:",
            policy.get(
                "consent_given"
            ),
        )

        print(
            "Affordability Score:",
            policy.get(
                "affordability_score"
            ),
        )

        print(
            "Confidence:",
            policy.get(
                "confidence"
            ),
        )

        print(
            "Risk Score:",
            policy.get(
                "risk_score"
            ),
        )

        print(
            "Critical:",
            policy.get(
                "critical"
            ),
        )

        print(
            "Policy Details:",
            policy.get(
                "policy"
            ),
        )

        # ========================================================
        # COMMUNICATION
        # ========================================================

        print("\nCOMMUNICATION")
        print("-" * 70)

        communication = result["communication"]

        print(
            "Agent:",
            communication.get(
                "agent"
            ),
        )

        print(
            "Language:",
            communication.get(
                "language"
            ),
        )

        print(
            "Policy Final Action:",
            communication.get(
                "policy_final_action"
            ),
        )

        print(
            "Policy Overridden:",
            communication.get(
                "policy_overridden"
            ),
        )

        print("\nCUSTOMER RESPONSE")
        print("-" * 70)

        print(
            communication.get(
                "response"
            )
        )

        # ========================================================
        # FINAL DECISION
        # ========================================================

        print("\nFINAL DECISION")
        print("-" * 70)

        final_decision = result[
            "final_decision"
        ]

        print(
            "Original Action:",
            final_decision.get(
                "original_action"
            ),
        )

        print(
            "Final Action:",
            final_decision.get(
                "final_action"
            ),
        )

        print(
            "Policy Overridden:",
            final_decision.get(
                "policy_overridden"
            ),
        )

        print(
            "Human Escalation:",
            final_decision.get(
                "human_escalation"
            ),
        )

        print(
            "Policy Failures:",
            final_decision.get(
                "policy_failures"
            ),
        )

        # ========================================================
        # SUCCESS
        # ========================================================

        print("\n" + "=" * 70)
        print("FINGURU ORCHESTRATOR TEST COMPLETE")
        print("=" * 70)

    except Exception as e:

        print("\n" + "=" * 70)
        print("ORCHESTRATOR ERROR")
        print("=" * 70)

        print(
            "Exception Type:",
            type(e).__name__,
        )

        print(
            "Exception:",
            str(e),
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()