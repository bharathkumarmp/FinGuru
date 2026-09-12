from app.database import SessionLocal
from app.services.transaction_anomaly import detect_transaction_anomaly


def main():
    db = SessionLocal()

    try:
        result = detect_transaction_anomaly(
            db=db,
            customer_id=1,
            transaction_id=27,
        )

        print("\n========================================")
        print("   TRANSACTION ANOMALY TEST")
        print("========================================\n")

        print("Customer ID:", result["customer_id"])
        print("Transaction ID:", result["transaction_id"])
        print("Anomaly Score:", result["anomaly_score"])
        print("Risk Level:", result["risk_level"])
        print("Recommended Action:", result["recommended_action"])

        print("\nReason:")
        print(result["reason"])

        print("\nSignals:")
        for key, value in result["signals"].items():
            print(f"  {key}: {value}")

        print("\nBaseline:")
        for key, value in result["baseline"].items():
            print(f"  {key}: {value}")

        print("\n========================================")
        print("   TRANSACTION ANOMALY TEST COMPLETE")
        print("========================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()