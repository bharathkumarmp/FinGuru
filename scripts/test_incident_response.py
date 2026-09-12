from app.database import SessionLocal
from app.services.incident_response import create_security_incident


def main():

    db = SessionLocal()

    try:

        result = create_security_incident(
            db=db,
            customer_id=1,
            threat_score=90,
            threat_level="CRITICAL",
            recommended_action="BLOCK_AND_ESCALATE",
            evidence=[
                "Critical fraud risk detected.",
                "Customer behavior deviates significantly from historical behavior.",
                "New device detected.",
                "New location detected.",
                "New beneficiary detected.",
                "Multiple critical security signals correlate to a potential account takeover.",
            ],
        )

        print("\n" + "=" * 60)
        print("FinGuru Incident Response")
        print("=" * 60)

        print("\nINCIDENT CREATED")
        print(result["incident_created"])

        if result["incident_created"]:

            incident = result["incident"]

            print("\nINCIDENT")

            for key, value in incident.items():
                print(f"{key}: {value}")

            print("\nRESPONSE WORKFLOW")

            workflow = result["response_workflow"]

            for key, value in workflow.items():

                if key == "evidence_timeline":

                    print("\nevidence_timeline:")

                    for item in value:
                        print(
                            f"  {item['sequence']}. "
                            f"{item['evidence']}"
                        )

                else:
                    print(f"{key}: {value}")

        print("\n" + "=" * 60)
        print("Incident Response test successful.")
        print("=" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()