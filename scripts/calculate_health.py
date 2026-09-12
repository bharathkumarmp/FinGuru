import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))


from app.database import SessionLocal

from app.services.financial_health import (
    calculate_all_health_scores,
)


def main():

    print("\nFinGuru Financial Health Engine")
    print("=" * 50)

    db = SessionLocal()

    try:

        results = calculate_all_health_scores(
            db
        )

        print("\nHealth calculation successful.")
        print(
            f"Customers processed: {len(results)}"
        )

    except Exception as exc:

        db.rollback()

        print(
            f"\nHealth calculation failed: {exc}"
        )

        raise

    finally:

        db.close()


if __name__ == "__main__":
    main()