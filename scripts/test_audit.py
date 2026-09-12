from app.database import SessionLocal
from app.services.audit import create_audit_log


def main():

    db = SessionLocal()

    try:

        audit = create_audit_log(
            db=db,
            action="SECURITY_INCIDENT_CREATED",
            resource="incident:2",
            customer_id=1,
            details={
                "threat_score": 90,
                "severity": "CRITICAL",
                "recommended_action": "BLOCK_AND_ESCALATE",
                "reason": "Multiple security signals correlated.",
            },
        )

        print("\n" + "=" * 60)
        print("FinGuru Audit Logging")
        print("=" * 60)

        print("\nAUDIT LOG CREATED")

        print("ID:", audit.id)
        print("Action:", audit.action)
        print("Resource:", audit.resource)
        print("Customer ID:", audit.customer_id)
        print("IP Address:", audit.ip_address)
        print("Details:", audit.details)
        print("Created At:", audit.created_at)

        print("\n" + "=" * 60)
        print("Audit Logging test successful.")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()