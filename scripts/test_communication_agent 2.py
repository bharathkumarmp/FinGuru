from app.database import SessionLocal

from app.agents.recommendation_agent import (
    recommendation_agent,
)

from app.agents.financial_agent import (
    financial_agent,
)

from app.agents.communication_agent import (
    communication_agent,
)


def main():

    db = SessionLocal()

    try:

        print("=" * 60)
        print("COMMUNICATION AGENT TEST")
        print("=" * 60)

        # ========================================================
        # 1. FINANCIAL ANALYST AGENT
        # ========================================================

        print("\n[1] Running Financial Analyst Agent...")

        financial_result = (
            financial_agent.analyze_customer(
                db=db,
                customer_id=1,
            )
        )

        print("✓ Financial Analyst Agent completed")

        # ========================================================
        # 2. RECOMMENDATION AGENT
        # ========================================================

        print("\n[2] Running Recommendation Agent...")

        recommendation_result = (
            recommendation_agent.analyze(
                db=db,
                customer_id=1,
                loan_requested=True,
                loan_amount=300000,
                tenure_months=36,
                interest_rate=12,
            )
        )

        print("✓ Recommendation Agent completed")

        # ========================================================
        # 3. COMMUNICATION AGENT
        # ========================================================

        print("\n[3] Running Communication Agent...")

        communication_result = (
            communication_agent.generate_response(
                recommendation_result=(
                    recommendation_result
                ),
                financial_result=(
                    financial_result
                ),
                language="English",
            )
        )

        print("✓ Communication Agent completed")

        # ========================================================
        # 4. DISPLAY RESULT
        # ========================================================

        print("\n" + "=" * 60)
        print("COMMUNICATION AGENT RESULT")
        print("=" * 60)

        print("\nAgent:")
        print(
            communication_result.get(
                "agent"
            )
        )

        print("\nCustomer ID:")
        print(
            communication_result.get(
                "customer_id"
            )
        )

        print("\nLanguage:")
        print(
            communication_result.get(
                "language"
            )
        )

        print("\nFinal Action:")
        print(
            communication_result.get(
                "action"
            )
        )

        print("\nLLM Ready:")
        print(
            communication_result.get(
                "llm_ready"
            )
        )

        # ========================================================
        # 5. CUSTOMER-FACING RESPONSE
        # ========================================================

        print("\n" + "-" * 60)
        print("FINAL CUSTOMER RESPONSE")
        print("-" * 60)

        print(
            communication_result.get(
                "response"
            )
        )

        print("-" * 60)

        # ========================================================
        # 6. STRUCTURED CONTEXT
        # ========================================================

        print("\n" + "=" * 60)
        print("STRUCTURED COMMUNICATION CONTEXT")
        print("=" * 60)

        structured_context = (
            communication_result.get(
                "structured_context",
                {},
            )
        )

        print("\nCustomer:")
        print(
            structured_context.get(
                "customer"
            )
        )

        print("\nFinancial State:")
        print(
            structured_context.get(
                "financial_state"
            )
        )

        print("\nFinancial Health:")
        print(
            structured_context.get(
                "financial_health"
            )
        )

        print("\nFinancial Stress:")
        print(
            structured_context.get(
                "financial_stress"
            )
        )

        print("\nRecommendation:")
        print(
            structured_context.get(
                "recommendation"
            )
        )

        print("\nLoan Analysis:")
        print(
            structured_context.get(
                "loan_analysis"
            )
        )

        print("\nNext Best Offer:")
        print(
            structured_context.get(
                "offer"
            )
        )

        # ========================================================
        # 7. COMPLETE
        # ========================================================

        print("\n" + "=" * 60)
        print("COMMUNICATION AGENT TEST COMPLETE")
        print("=" * 60)

    except Exception as e:

        print("\n" + "=" * 60)
        print("ERROR")
        print("=" * 60)

        print("\nException Type:")
        print(type(e).__name__)

        print("\nException:")
        print(str(e))

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()