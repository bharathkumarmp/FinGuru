import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.services.life_events import detect_life_events


def main():
    print("\nFinGuru Life-Event Detection")
    print("=" * 60)

    db = SessionLocal()

    try:
        result = detect_life_events(
            db=db,
            customer_id=1,
        )

        print(
            f"\nCustomer: "
            f"{result['customer_name']}"
        )

        print(
            f"Events detected: "
            f"{result['event_count']}"
        )

        print("\nDetected Events:")

        for event in result["events"]:
            print(
                f"  {event['event_type']:<22} "
                f"confidence={event['confidence']:.2f}"
            )

            print(
                f"    {event.get('description', '')}"
            )

        print("\nLife-event detection successful.")

    except Exception as exc:
        db.rollback()
        print(
            f"\nLife-event detection failed: {exc}"
        )
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
