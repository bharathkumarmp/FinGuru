import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))


from app.database import SessionLocal

from app.services.loan_risk import (
    evaluate_customer_loan,
)


def main():

    print("\nFinGuru Loan Risk Engine")
    print("=" * 50)

    db = SessionLocal()

    try:

        # Demo scenario:
        # Customer 1 asks for ₹3,00,000
        # over 36 months at 12% annual interest.

        customer_id = 1
        loan_amount = 300000
        tenure_months = 36
        interest_rate = 12.0

        result = evaluate_customer_loan(
            db=db,
            customer_id=customer_id,
            loan_amount=loan_amount,
            tenure_months=tenure_months,
            interest_rate=interest_rate,
        )

        print("\nLoan Simulation")
        print("-" * 50)

        print(
            f"Customer: "
            f"{result['customer_id']}"
        )

        print(
            f"Loan amount: "
            f"₹{result['loan_amount']:,.2f}"
        )

        print(
            f"Tenure: "
            f"{result['tenure_months']} months"
        )

        print(
            f"Interest rate: "
            f"{result['interest_rate']}%"
        )

        print(
            f"Current EMI: "
            f"₹{result['current_emi']:,.2f}"
        )

        print(
            f"Proposed EMI: "
            f"₹{result['proposed_emi']:,.2f}"
        )

        print(
            f"Projected EMI ratio: "
            f"{result['projected_emi_ratio']:.2%}"
        )

        print(
            f"Projected monthly surplus: "
            f"₹{result['projected_surplus']:,.2f}"
        )

        print(
            f"Risk score: "
            f"{result['risk_score']}/100"
        )

        print(
            f"Risk level: "
            f"{result['risk_level']}"
        )

        print(
            f"Suitability: "
            f"{result['suitability']}"
        )

        print("\nReasons:")

        for reason in result["reasons"]:

            print(
                f"  • {reason}"
            )

        print(
            "\n✓ Loan risk analysis successful."
        )

    except Exception as exc:

        print(
            f"\n✗ Loan risk analysis failed: "
            f"{exc}"
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()