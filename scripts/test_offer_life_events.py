from app.services.offer_engine import generate_next_best_offer


print("=" * 60)
print("FINGURU LIFE EVENT → NEXT BEST OFFER TEST")
print("=" * 60)


# ============================================================
# HEALTHY CUSTOMER + SALARY CREDITED
# ============================================================

result = generate_next_best_offer(
    health_score=82.0,
    stress_score=18.0,
    monthly_surplus=30000.0,
    savings_rate=0.10,
    emi_ratio=0.20,
    income_stability=90.0,
    consent_given=True,
    life_events=[
        {
            "event_type": "SALARY_CREDITED",
            "confidence": 0.98,
        }
    ],
)


print("\nHealthy Customer + Salary Credited")
print("-" * 60)

print("Best Offer  :", result["offer"])
print("Score       :", result["offer_score"])
print("Reason      :", result["reason"])

print("\nOffers:")

for offer in result["offers"]:
    print(
        f"  {offer['offer_type']} "
        f"| Score: {offer['score']} "
        f"| Priority: {offer['priority']}"
    )


# ============================================================
# STRESSED CUSTOMER + SPENDING SPIKE
# ============================================================

result = generate_next_best_offer(
    health_score=45.0,
    stress_score=55.0,
    monthly_surplus=5000.0,
    savings_rate=0.05,
    emi_ratio=0.35,
    income_stability=60.0,
    consent_given=True,
    life_events=[
        {
            "event_type": "SPENDING_SPIKE",
            "confidence": 0.90,
        }
    ],
)


print("\nStressed Customer + Spending Spike")
print("-" * 60)

print("Best Offer  :", result["offer"])
print("Score       :", result["offer_score"])
print("Reason      :", result["reason"])

print("\nOffers:")

for offer in result["offers"]:
    print(
        f"  {offer['offer_type']} "
        f"| Score: {offer['score']} "
        f"| Priority: {offer['priority']}"
    )


print("\n" + "=" * 60)
print("LIFE EVENT OFFER TEST COMPLETE")
print("=" * 60)