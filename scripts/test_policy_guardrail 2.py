from app.policy.policy_engine import policy_engine


def run_test(name, **kwargs):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = policy_engine.evaluate(**kwargs)

    print("Policy Passed :", result["policy_passed"])
    print("Final Action  :", result["final_action"])
    print("Failed Checks :", result["failed_checks"])
    print(
        "Human Escalation :",
        result["human_escalation"]["required"],
    )


# ============================================================
# TEST 1 — HEALTHY CUSTOMER
# ============================================================

run_test(
    "TEST 1 — HEALTHY CUSTOMER",

    consent_given=True,

    requested_purpose="financial_advice",

    allowed_purposes=[
        "financial_advice",
        "loan_recommendation",
        "fraud_detection",
        "financial_analysis",
    ],

    affordability_score=85,

    projected_emi_ratio=0.25,

    monthly_surplus=30000,

    confidence=0.90,

    risk_score=10,

    bias_score=0.05,

    compliance_passed=True,

    critical=False,
)


# ============================================================
# TEST 2 — NEGATIVE CASH FLOW
# ============================================================

run_test(
    "TEST 2 — NEGATIVE CASH FLOW",

    consent_given=True,

    requested_purpose="financial_advice",

    allowed_purposes=[
        "financial_advice",
        "loan_recommendation",
        "fraud_detection",
        "financial_analysis",
    ],

    affordability_score=15,

    projected_emi_ratio=0.58,

    monthly_surplus=-43000,

    confidence=0.85,

    risk_score=63,

    bias_score=0.05,

    compliance_passed=True,

    critical=False,
)


# ============================================================
# TEST 3 — NO CONSENT
# ============================================================

run_test(
    "TEST 3 — NO CONSENT",

    consent_given=False,

    requested_purpose="financial_advice",

    allowed_purposes=[
        "financial_advice",
        "loan_recommendation",
        "fraud_detection",
        "financial_analysis",
    ],

    affordability_score=85,

    projected_emi_ratio=0.25,

    monthly_surplus=30000,

    confidence=0.90,

    risk_score=10,

    bias_score=0.05,

    compliance_passed=True,

    critical=False,
)


# ============================================================
# TEST 4 — CRITICAL SECURITY EVENT
# ============================================================

run_test(
    "TEST 4 — CRITICAL SECURITY EVENT",

    consent_given=True,

    requested_purpose="fraud_detection",

    allowed_purposes=[
        "financial_advice",
        "loan_recommendation",
        "fraud_detection",
        "financial_analysis",
    ],

    affordability_score=80,

    projected_emi_ratio=0.20,

    monthly_surplus=50000,

    confidence=0.95,

    risk_score=90,

    bias_score=0.05,

    compliance_passed=True,

    critical=True,
)


print("\n" + "=" * 60)
print("POLICY GUARDRAIL TEST COMPLETE")
print("=" * 60)