from app.policy.policy_engine import policy_engine


def main():

    result = policy_engine.evaluate(

        # ----------------------------------------------------
        # Consent
        # ----------------------------------------------------

        consent_given=True,

        # ----------------------------------------------------
        # Purpose
        # ----------------------------------------------------

        requested_purpose="loan_recommendation",

        allowed_purposes=[
            "loan_recommendation",
            "financial_advice",
            "fraud_detection",
        ],

        # ----------------------------------------------------
        # Affordability
        # ----------------------------------------------------

        affordability_score=75.0,

        projected_emi_ratio=0.30,

        monthly_surplus=25000.0,

        # ----------------------------------------------------
        # AI confidence
        # ----------------------------------------------------

        confidence=0.90,

        # ----------------------------------------------------
        # Risk
        # ----------------------------------------------------

        risk_score=10.0,

        # ----------------------------------------------------
        # Bias
        # ----------------------------------------------------

        bias_score=0.05,

        # ----------------------------------------------------
        # Compliance
        # ----------------------------------------------------

        compliance_passed=True,

        compliance_reason=(
            "No compliance violation detected."
        ),

        # ----------------------------------------------------
        # Critical flag
        # ----------------------------------------------------

        critical=False,
    )

    print()
    print("========================================")
    print("       FINGURU POLICY ENGINE TEST")
    print("========================================")

    print(
        "Policy Passed :",
        result["policy_passed"]
    )

    print(
        "Final Action  :",
        result["final_action"]
    )

    print()
    print("------------- POLICY CHECKS ------------")

    for name, check in result["checks"].items():

        print(
            f"{name:25} : "
            f"{check.get('passed', 'N/A')}"
        )

    print()
    print("---------- HUMAN ESCALATION ------------")

    print(
        "Required:",
        result["human_escalation"]["required"]
    )

    if result["human_escalation"]["reasons"]:
        print("Reasons:")

        for reason in result["human_escalation"]["reasons"]:
            print("-", reason)

    print()
    print("========================================")
    print()


if __name__ == "__main__":
    main()