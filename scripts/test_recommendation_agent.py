from app.database import SessionLocal
from app.agents.recommendation_agent import recommendation_agent


def main():

    db = SessionLocal()

    try:

        print("=" * 60)
        print("RECOMMENDATION AGENT TEST")
        print("=" * 60)

        result = recommendation_agent.analyze(
            db=db,
            customer_id=1,
            loan_requested=True,
            loan_amount=300000,
            tenure_months=36,
            interest_rate=12,
        )

        print("\nAgent:")
        print(result["agent"])

        print("\nCustomer:")
        print(result["customer"])

        print("\nFinancial State:")
        print(result["financial_state"])

        print("\nFinancial Health:")
        print(result["financial_health"])

        print("\nFinancial Stress:")
        print(result["financial_stress"])

        print("\nLife Events:")
        print(result["life_events"])

        print("\nLoan Analysis:")
        print(result["loan_analysis"])

        print("\nNext Best Action:")
        print(result["next_best_action"])

        print("\nNext Best Offer:")
        print(result["next_best_offer"])

        print("\nAgent Reasoning:")
        print(result["agent_reasoning"])

        print("\n")
        print("=" * 60)
        print("RECOMMENDATION AGENT TEST COMPLETE")
        print("=" * 60)

    except Exception as e:

        print("\nERROR:")
        print(type(e).__name__)
        print(str(e))

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()