from app.database import Base, engine

# Import every model so SQLAlchemy registers all tables.
from app.models import (
    User,
    Customer,
    Account,
    Transaction,
    Loan,
    EMIRecord,
    CustomerFeatures,
    FinancialHealth,
    FinancialStress,
    FraudEvent,
    Recommendation,
    Consent,
    AuditLog,
    Incident,
    Product,
)


def init_db():
    print("Creating FinGuru database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")

    print("\nTables:")
    for table in Base.metadata.sorted_tables:
        print(f"  ✓ {table.name}")


if __name__ == "__main__":
    init_db()
