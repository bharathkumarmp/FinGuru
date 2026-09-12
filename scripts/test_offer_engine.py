from app.services.offer_engine import generate_next_best_offer


print("=" * 60)
print("FINGURU NEXT BEST OFFER ENGINE TEST")
print("=" * 60)


# ============================================================
# CUSTOMER 1
# Financially stressed customer
# ============================================================

result = generate_next_best_offer(
    health_score=37.0,
    stress_score=63.0,
    monthly_surplus=-43320.75,
    savings_rate=0.0,
    emi_ratio=0.0,
    income_stability=50.0,
    consent_given=True,
)


print("\nCustomer 1")
print("-" * 60)

print("Best Offer       :", result["offer"])
print("Offer Score      :", result["offer_score"])
print("Reason           :", result["reason"])

print("\nAvailable Offers:")

for offer in result["offers"]:
    print(
        f"  {offer['offer_type']} "
        f"| Score: {offer['score']} "
        f"| Priority: {offer['priority']}"
    )


# ============================================================
# NO CONSENT TEST
# ============================================================

result_no_consent = generate_next_best_offer(
    health_score=80.0,
    stress_score=20.0,
    monthly_surplus=20000.0,
    savings_rate=0.25,
    emi_ratio=0.20,
    income_stability=90.0,
    consent_given=False,
)


print("\nNo Consent Test")
print("-" * 60)

print("Best Offer       :", result_no_consent["offer"])
print("Offer Score      :", result_no_consent["offer_score"])
print("Reason           :", result_no_consent["reason"])


print("\n" + "=" * 60)
print("OFFER ENGINE TEST COMPLETE")
print("=" * 60)