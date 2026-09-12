from app.database import SessionLocal
from app.agents.financial_agent import financial_agent


db = SessionLocal()

try:
    print("=" * 60)
    print("FINANCIAL ANALYST AGENT TEST")
    print("=" * 60)

    result = financial_agent.analyze_customer(
        db=db,
        customer_id=1,
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

    print("\nStrengths:")
    print(result["strengths"])

    print("\nConcerns:")
    print(result["concerns"])

    print("\nOverall Assessment:")
    print(result["overall_assessment"])

    print("\nFINANCIAL AGENT TEST COMPLETE")

finally:
    db.close()