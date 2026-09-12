import sys
import json
from pathlib import Path

import pandas as pd
from sqlalchemy import delete


# ============================================================
# PATH CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent

BACKEND_DIR = ROOT / "backend"
DATA_DIR = ROOT / "data"

# Allow imports such as:
# from app.database import SessionLocal
sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# FIN GURU APPLICATION IMPORTS
# ============================================================

from app.database import SessionLocal

from app.models import (
    Customer,
    Account,
    Transaction,
    Loan,
    EMIRecord,
    FraudEvent,
    Product,
)


# ============================================================
# CSV LOADER
# ============================================================

def load_csv(filename):
    """
    Load a CSV file from the data directory.
    """

    path = DATA_DIR / filename

    print(f"Loading {path}...")

    if not path.exists():
        raise FileNotFoundError(
            f"Data file not found: {path}"
        )

    return pd.read_csv(path)


# ============================================================
# CLEAR EXISTING DATA
# ============================================================

def clear_existing_data(db):
    """
    Delete previously seeded banking data.

    Child/dependent records are deleted first.
    """

    print("\nClearing existing banking data...")

    # Delete dependent records first
    db.execute(delete(FraudEvent))
    db.execute(delete(EMIRecord))
    db.execute(delete(Transaction))
    db.execute(delete(Loan))
    db.execute(delete(Account))
    db.execute(delete(Customer))
    db.execute(delete(Product))

    db.commit()

    print("Existing data cleared.")


# ============================================================
# SEED CUSTOMERS
# ============================================================

def seed_customers(db):
    """
    Insert customer records from customers.csv.
    """

    df = load_csv("customers.csv")

    records = []

    for _, row in df.iterrows():

        records.append(
            Customer(
                id=int(row["id"]),

                customer_code=str(
                    row["customer_code"]
                ),

                full_name=str(
                    row["full_name"]
                ),

                email=str(
                    row["email"]
                ),

                phone=str(
                    row["phone"]
                ),

                date_of_birth=pd.to_datetime(
                    row["date_of_birth"]
                ).date(),

                city=str(
                    row["city"]
                ),

                occupation=str(
                    row["occupation"]
                ),

                monthly_income=float(
                    row["monthly_income"]
                ),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Customers inserted: {len(records)}"
    )


# ============================================================
# SEED ACCOUNTS
# ============================================================

def seed_accounts(db):
    """
    Insert account records from accounts.csv.
    """

    df = load_csv("accounts.csv")

    records = []

    for _, row in df.iterrows():

        records.append(
            Account(
                id=int(row["id"]),

                customer_id=int(
                    row["customer_id"]
                ),

                account_number=str(
                    row["account_number"]
                ),

                account_type=str(
                    row["account_type"]
                ),

                balance=float(
                    row["balance"]
                ),

                currency=str(
                    row["currency"]
                ),

                status=str(
                    row["status"]
                ),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Accounts inserted: {len(records)}"
    )


# ============================================================
# SEED TRANSACTIONS
# ============================================================

def seed_transactions(db):
    """
    Insert transaction records from transactions.csv.
    """

    df = load_csv("transactions.csv")

    records = []

    for _, row in df.iterrows():

        # Handle optional beneficiary
        beneficiary = row["beneficiary"]

        if pd.isna(beneficiary):
            beneficiary = None
        else:
            beneficiary = str(beneficiary)

        records.append(
            Transaction(
                id=int(row["id"]),

                customer_id=int(
                    row["customer_id"]
                ),

                account_id=int(
                    row["account_id"]
                ),

                transaction_type=str(
                    row["transaction_type"]
                ),

                amount=float(
                    row["amount"]
                ),

                merchant=str(
                    row["merchant"]
                ),

                category=str(
                    row["category"]
                ),

                location=str(
                    row["location"]
                ),

                device_id=str(
                    row["device_id"]
                ),

                beneficiary=beneficiary,

                description=str(
                    row["description"]
                ),

                timestamp=pd.to_datetime(
                    row["timestamp"]
                ).to_pydatetime(),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Transactions inserted: {len(records)}"
    )


# ============================================================
# SEED LOANS
# ============================================================

def seed_loans(db):
    """
    Insert loan records from loans.csv.
    """

    df = load_csv("loans.csv")

    records = []

    for _, row in df.iterrows():

        records.append(
            Loan(
                id=int(row["id"]),

                customer_id=int(
                    row["customer_id"]
                ),

                loan_type=str(
                    row["loan_type"]
                ),

                principal_amount=float(
                    row["principal_amount"]
                ),

                interest_rate=float(
                    row["interest_rate"]
                ),

                tenure_months=int(
                    row["tenure_months"]
                ),

                monthly_emi=float(
                    row["monthly_emi"]
                ),

                outstanding_amount=float(
                    row["outstanding_amount"]
                ),

                status=str(
                    row["status"]
                ),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Loans inserted: {len(records)}"
    )


# ============================================================
# SEED EMI RECORDS
# ============================================================

def seed_emi_records(db):
    """
    Insert EMI records from emi_records.csv.
    """

    df = load_csv("emi_records.csv")

    records = []

    for _, row in df.iterrows():

        # paid_at is optional
        paid_at = None

        if pd.notna(row["paid_at"]):

            paid_at = pd.to_datetime(
                row["paid_at"]
            ).to_pydatetime()

        records.append(
            EMIRecord(
                id=int(row["id"]),

                loan_id=int(
                    row["loan_id"]
                ),

                customer_id=int(
                    row["customer_id"]
                ),

                due_date=pd.to_datetime(
                    row["due_date"]
                ).date(),

                amount=float(
                    row["amount"]
                ),

                paid_amount=float(
                    row["paid_amount"]
                ),

                status=str(
                    row["status"]
                ),

                paid_at=paid_at,
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ EMI records inserted: {len(records)}"
    )


# ============================================================
# SEED FRAUD EVENTS
# ============================================================

def seed_fraud_events(db):
    """
    Insert fraud event records from fraud_events.csv.
    """

    df = load_csv("fraud_events.csv")

    records = []

    for _, row in df.iterrows():

        # transaction_id is optional
        transaction_id = row["transaction_id"]

        if pd.isna(transaction_id):

            transaction_id = None

        else:

            transaction_id = int(
                transaction_id
            )

        records.append(
            FraudEvent(
                id=int(row["id"]),

                customer_id=int(
                    row["customer_id"]
                ),

                transaction_id=transaction_id,

                fraud_score=float(
                    row["fraud_score"]
                ),

                risk_level=str(
                    row["risk_level"]
                ),

                status=str(
                    row["status"]
                ),

                reason=str(
                    row["reason"]
                ),

                anomaly_score=float(
                    row["anomaly_score"]
                ),

                rule_score=float(
                    row["rule_score"]
                ),

                identity_risk_score=float(
                    row["identity_risk_score"]
                ),

                recommended_action=str(
                    row["recommended_action"]
                ),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Fraud events inserted: {len(records)}"
    )


# ============================================================
# SEED PRODUCTS
# ============================================================

def seed_products(db):
    """
    Insert financial products from products.json.
    """

    path = DATA_DIR / "products.json"

    print(f"Loading {path}...")

    if not path.exists():

        raise FileNotFoundError(
            f"Product file not found: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:

        products = json.load(file)

    records = []

    for index, product in enumerate(
        products,
        start=1,
    ):

        records.append(
            Product(
                id=index,

                product_code=product[
                    "product_code"
                ],

                name=product[
                    "name"
                ],

                product_type=product[
                    "product_type"
                ],

                description=product.get(
                    "description"
                ),

                interest_rate=product.get(
                    "interest_rate"
                ),

                min_amount=product.get(
                    "min_amount"
                ),

                max_amount=product.get(
                    "max_amount"
                ),

                active=product.get(
                    "active",
                    True,
                ),
            )
        )

    db.add_all(records)

    db.commit()

    print(
        f"✓ Products inserted: {len(records)}"
    )


# ============================================================
# DATABASE VERIFICATION
# ============================================================

def verify_database(db):
    """
    Print record counts after seeding.
    """

    print("\nDatabase verification:")
    print("=" * 50)

    tables = [
        ("Customers", Customer),
        ("Accounts", Account),
        ("Transactions", Transaction),
        ("Loans", Loan),
        ("EMI Records", EMIRecord),
        ("Fraud Events", FraudEvent),
        ("Products", Product),
    ]

    for name, model in tables:

        count = db.query(model).count()

        print(
            f"{name:<20}: {count}"
        )

    print("=" * 50)


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nFinGuru Database Seeder")
    print("=" * 50)

    print(f"Project root : {ROOT}")
    print(f"Data folder  : {DATA_DIR}")
    print(f"Backend      : {BACKEND_DIR}")

    db = SessionLocal()

    try:

        # ----------------------------------------------------
        # 1. Clear previous data
        # ----------------------------------------------------

        clear_existing_data(db)

        # ----------------------------------------------------
        # 2. Seed customers
        # ----------------------------------------------------

        seed_customers(db)

        # ----------------------------------------------------
        # 3. Seed accounts
        # ----------------------------------------------------

        seed_accounts(db)

        # ----------------------------------------------------
        # 4. Seed transactions
        # ----------------------------------------------------

        seed_transactions(db)

        # ----------------------------------------------------
        # 5. Seed loans
        # ----------------------------------------------------

        seed_loans(db)

        # ----------------------------------------------------
        # 6. Seed EMI records
        # ----------------------------------------------------

        seed_emi_records(db)

        # ----------------------------------------------------
        # 7. Seed fraud events
        # ----------------------------------------------------

        seed_fraud_events(db)

        # ----------------------------------------------------
        # 8. Seed financial products
        # ----------------------------------------------------

        seed_products(db)

        # ----------------------------------------------------
        # 9. Verify database
        # ----------------------------------------------------

        verify_database(db)

        print(
            "\n✓ FinGuru database seeded successfully."
        )

    except Exception as exc:

        db.rollback()

        print(
            f"\n✗ Database seeding failed: {exc}"
        )

        raise

    finally:

        db.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()