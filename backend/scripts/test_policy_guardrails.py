from app.policy.guardrails import policy_guardrail


def main():

    result = policy_guardrail.evaluate(
        consent_given=True,

        requested_purpose="loan_recommendation",

        allowed_purposes=[
            "loan_recommendation",
            "financial_advice",
            "fraud_detection",
        ],

        affordability_score=75.0,

        projected_emi_ratio=0.30,

        monthly_surplus=25000.0,

        confidence=0.90,

        risk_score=10.0,

        bias_score=0.05,

        compliance_passed=True,

        compliance_reason=(
            "No compliance violation detected."
        ),

        critical=False,
    )

    print("\n========================================")
    print("POLICY GUARDRAIL TEST")
    print("========================================")

    print(
        "Policy Passed:",
        result["policy_passed"]
    )

    print(
        "Final Action:",
        result["final_action"]
    )

    print("\nChecks:")

    for name, check in result["checks"].items():
        print(
            f"{name}: "
            f"{check.get('passed', 'N/A')}"
        )

    print("\nHuman Escalation:")
    print(
        result["human_escalation"]
    )

    print("========================================\n")


if __name__ == "__main__":
    main()