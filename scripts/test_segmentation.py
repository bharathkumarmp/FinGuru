import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.services.segmentation import generate_customer_segments


def main():
    print("\nFinGuru Customer Segmentation")
    print("=" * 60)

    db = SessionLocal()

    try:
        result = generate_customer_segments(
            db=db,
            n_clusters=5,
        )

        print(f"\nClusters: {result['cluster_count']}")

        print("\nCluster Names:")
        for cluster_id, name in result["cluster_names"].items():
            print(f"  Cluster {cluster_id}: {name}")

        print("\nCustomer Samples:")

        for customer in result["segments"][:10]:
            print(
                f"  Customer {customer['customer_id']:>3} | "
                f"{customer['customer_name']:<25} | "
                f"Cluster {customer['cluster']} | "
                f"{customer['segment']}"
            )

        print(
            f"\nTotal customers segmented: "
            f"{len(result['segments'])}"
        )

        print("\nSegmentation successful.")

    except Exception as exc:
        db.rollback()
        print(f"\nSegmentation failed: {exc}")
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
