from sqlalchemy.orm import Session
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from app.models import Customer, CustomerFeatures


FEATURE_COLUMNS = [
    "avg_monthly_income",
    "avg_monthly_spending",
    "savings_rate",
    "emi_ratio",
    "credit_utilization",
    "missed_emi_count",
    "transaction_frequency",
    "spending_growth",
    "balance_volatility",
    "income_stability",
    "cash_buffer",
]


def get_customer_feature_matrix(db: Session):
    rows = (
        db.query(CustomerFeatures)
        .order_by(CustomerFeatures.customer_id)
        .all()
    )

    if not rows:
        raise ValueError("No customer features found")

    data = []

    for row in rows:
        data.append([
            float(getattr(row, column, 0) or 0)
            for column in FEATURE_COLUMNS
        ])

    return rows, data


def train_customer_segments(
    db: Session,
    n_clusters: int = 5,
):
    rows, data = get_customer_feature_matrix(db)

    if len(rows) < n_clusters:
        n_clusters = len(rows)

    if n_clusters < 2:
        raise ValueError("At least two customers are required for segmentation")

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10,
    )

    labels = model.fit_predict(scaled_data)

    segments = []

    for row, label in zip(rows, labels):
        customer = (
            db.query(Customer)
            .filter(Customer.id == row.customer_id)
            .first()
        )

        segments.append({
            "customer_id": row.customer_id,
            "customer_name": customer.full_name if customer else None,
            "cluster": int(label),
            "features": {
                column: round(
                    float(getattr(row, column, 0) or 0),
                    4,
                )
                for column in FEATURE_COLUMNS
            },
        })

    return {
        "model": model,
        "scaler": scaler,
        "segments": segments,
    }


def describe_cluster(
    segments,
    cluster_id,
):
    cluster_customers = [
        item
        for item in segments
        if item["cluster"] == cluster_id
    ]

    if not cluster_customers:
        return "Unknown"

    def average(field):
        values = [
            item["features"][field]
            for item in cluster_customers
        ]

        return sum(values) / len(values)

    income = average("avg_monthly_income")
    savings = average("savings_rate")
    emi_ratio = average("emi_ratio")
    spending_growth = average("spending_growth")
    stability = average("income_stability")
    missed_emi = average("missed_emi_count")

    # Explain cluster using financial characteristics.
    if stability >= 0.80 and savings >= 0.20 and emi_ratio <= 0.30:
        return "High-Value Stable"

    if savings >= 0.20:
        return "High Savers"

    if emi_ratio >= 0.40 or missed_emi >= 2:
        return "Credit Dependent"

    if spending_growth >= 0.15 or stability < 0.40:
        return "Financially Stressed"

    if income < 60000:
        return "Young / Emerging Salaried"

    return "Balanced Financial Customer"


def generate_customer_segments(
    db: Session,
    n_clusters: int = 5,
):
    result = train_customer_segments(
        db=db,
        n_clusters=n_clusters,
    )

    segments = result["segments"]

    cluster_names = {}

    for cluster_id in sorted(
        set(item["cluster"] for item in segments)
    ):
        cluster_names[cluster_id] = describe_cluster(
            segments,
            cluster_id,
        )

    for item in segments:
        item["segment"] = cluster_names[item["cluster"]]

    return {
        "cluster_count": n_clusters,
        "segments": segments,
        "cluster_names": cluster_names,
    }


def get_customer_segment(
    db: Session,
    customer_id: int,
):
    result = generate_customer_segments(db)

    for item in result["segments"]:
        if item["customer_id"] == customer_id:
            return item

    raise ValueError(
        f"Customer {customer_id} not found in segmentation"
    )
