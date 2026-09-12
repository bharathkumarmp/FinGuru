import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.services.feature_engineering import (
    calculate_all_customer_features,
)


def main():

    print("\nFinGuru Feature Engineering")
    print("=" * 50)

    db = SessionLocal()

    try:

        results = calculate_all_customer_features(
            db
        )

        print("\nFeature generation successful.")
        print(
            f"Customers processed: {len(results)}"
        )

    except Exception as exc:

        db.rollback()

        print(
            f"\nFeature generation failed: {exc}"
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()