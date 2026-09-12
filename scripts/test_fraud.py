import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.services.fraud_detection import (
    analyze_all_transactions,
    save_fraud_results,
)


def main():

    print("\nFinGuru Fraud Detection Engine")
    print("=" * 50)

    db = SessionLocal()

    try:

        # Test first 100 transactions.
        # This validates the engine without
        # creating thousands of duplicate
        # fraud records.

        results = analyze_all_transactions(
            db,
            limit=100,
        )

        print(
            f"\nTransactions analyzed: "
            f"{len(results)}"
        )

        # Only save transactions that have
        # meaningful fraud signals.

        meaningful_results = [
            item
            for item in results
            if item[1]["fraud_score"] >= 30
        ]

        saved = save_fraud_results(
            db,
            meaningful_results,
        )

        print(
            f"Fraud events saved: {saved}"
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        if results:

            scores = [
                result["fraud_score"]
                for _, result in results
            ]

            high_risk = sum(
                1
                for score in scores
                if score >= 50
            )

            medium_risk = sum(
                1
                for score in scores
                if 30 <= score < 50
            )

            print("\nFraud Analysis Summary")
            print("-" * 40)

            print(
                f"Average fraud score: "
                f"{sum(scores) / len(scores):.2f}"
            )

            print(
                f"Medium risk: {medium_risk}"
            )

            print(
                f"High/Critical risk: {high_risk}"
            )

    except Exception as exc:

        db.rollback()

        print(
            f"\nFraud analysis failed: {exc}"
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()