from app.database import SessionLocal
from app.services.digital_twin import simulate_financial_future


def main():
    db = SessionLocal()

    try:
        result = simulate_financial_future(
            db=db,
            customer_id=1,
            loan_amount=300000,
            tenure_months=24,
            interest_rate=12,
        )

        print("\n" + "=" * 60)
        print("FinGuru Digital Twin Simulation")
        print("=" * 60)

        print("\nCUSTOMER")
        print("Customer ID:", result.get("customer_id"))

        print("\nALL RESULT KEYS")
        print(list(result.keys()))

        print("\nCURRENT FINANCIAL STATE")
        for key, value in result.get("current_state", {}).items():
            print(f"{key}: {value}")

        print("\nSIMULATION DETAILS")

        # Support whichever key the service currently returns
        loan = (
            result.get("loan_simulation")
            or result.get("loan")
            or result.get("simulation")
            or {}
        )

        if loan:
            for key, value in loan.items():
                print(f"{key}: {value}")
        else:
            print("No separate loan-simulation object returned.")

        print("\nPROJECTED FINANCIAL STATE")
        for key, value in result.get("projected_state", {}).items():
            print(f"{key}: {value}")

        print("\nIMPACT")
        for key, value in result.get("impact", {}).items():
            print(f"{key}: {value}")

        print("\nRECOMMENDATION")
        print(result.get("recommendation"))

        print("\nREASONS")
        for reason in result.get("reasons", []):
            print("-", reason)

        print("\n" + "=" * 60)
        print("Digital Twin simulation completed.")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()