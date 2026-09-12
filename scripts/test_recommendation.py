from app.services.recommendation_engine import generate_recommendation


def main():

    result = generate_recommendation(
        health_score=37,
        stress_score=63,
        monthly_income=24267.11,
        monthly_surplus=-43320.75,
        projected_emi_ratio=0.5819,
        loan_suitable=False,
        fraud_risk=0,
        customer_preference=50,
        loan_requested=True,
    )

    print("\n" + "=" * 60)
    print("FinGuru Recommendation Engine")
    print("=" * 60)

    print("\nRECOMMENDATION")
    print(result["recommendation"])

    print("\nRECOMMENDATION SCORE")
    print(result["recommendation_score"])

    print("\nSIGNALS")

    for key, value in result["signals"].items():
        print(f"{key}: {value}")

    print("\nGUARDRAILS")

    for key, value in result["guardrails"].items():
        print(f"{key}: {value}")

    print("\nREASONS")

    for reason in result["reasons"]:
        print("-", reason)

    print("\n" + "=" * 60)
    print("Recommendation Engine test successful.")
    print("=" * 60)


if __name__ == "__main__":
    main()