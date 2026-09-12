from app.database import SessionLocal
from app.services.identity_risk import analyze_identity_risk


def main():

    db = SessionLocal()

    try:

        result = analyze_identity_risk(
            db=db,
            customer_id=1,
        )

        print("\n" + "=" * 60)
        print("FinGuru Identity Risk Engine")
        print("=" * 60)

        print("\nCUSTOMER")
        print("Customer ID:", result["customer_id"])

        print("\nTRANSACTION")
        print("Transaction ID:", result["transaction_id"])

        print("\nIDENTITY STATUS")
        print(result["identity_status"])

        print("\nIDENTITY RISK SCORE")
        print(result["identity_risk_score"])

        print("\nRISK LEVEL")
        print(result["risk_level"])

        print("\nSIGNALS")

        for key, value in result["signals"].items():
            print(f"{key}: {value}")

        print("\nBASELINE")

        for key, value in result["baseline"].items():
            print(f"{key}: {value}")

        print("\nREASONS")

        for reason in result["reasons"]:
            print("-", reason)

        print("\n" + "=" * 60)
        print("Identity Risk test successful.")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()