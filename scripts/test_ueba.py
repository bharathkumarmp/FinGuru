from app.database import SessionLocal
from app.services.ueba import analyze_customer_behavior


def main():

    db = SessionLocal()

    try:

        result = analyze_customer_behavior(
            db=db,
            customer_id=1,
        )

        print("\n" + "=" * 60)
        print("FinGuru UEBA")
        print("=" * 60)

        print("\nCUSTOMER")
        print("Customer ID:", result["customer_id"])

        print("\nTRANSACTION")
        print("Transaction ID:", result["transaction_id"])

        print("\nBEHAVIOR STATUS")
        print(result["behavior_status"])

        print("\nUEBA SCORE")
        print(result["ueba_score"])

        print("\nRISK LEVEL")
        print(result["risk_level"])

        print("\nBASELINE")

        for key, value in result["baseline"].items():
            print(f"{key}: {value}")

        print("\nBEHAVIOR SIGNALS")

        for key, value in result["behavior_signals"].items():
            print(f"{key}: {value}")

        print("\nANOMALIES")

        for anomaly in result["anomalies"]:
            print("-", anomaly)

        print("\n" + "=" * 60)
        print("UEBA test successful.")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()