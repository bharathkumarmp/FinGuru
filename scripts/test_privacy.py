from app.privacy.pii_detection import detect_pii
from app.privacy.masking import mask_email, mask_phone
from app.privacy.tokenization import tokenize
from app.privacy.data_minimization import minimize_customer_data
from app.privacy.consent_manager import consent_manager


def main():

    print()
    print("========================================")
    print("         FINGURU PRIVACY TEST")
    print("========================================")

    # --------------------------------------------------------
    # PII Detection
    # --------------------------------------------------------

    pii_result = detect_pii(
        "Customer email is arjun@example.com "
        "and phone is 9876543210"
    )

    print()
    print("PII Detection:")
    print(pii_result)

    # --------------------------------------------------------
    # Email masking
    # --------------------------------------------------------

    print()
    print("Email Masking:")

    print(
        mask_email(
            "arjun@example.com"
        )
    )

    # --------------------------------------------------------
    # Phone masking
    # --------------------------------------------------------

    print()
    print("Phone Masking:")

    print(
        mask_phone(
            "9876543210"
        )
    )

    # --------------------------------------------------------
    # Tokenization
    # --------------------------------------------------------

    print()
    print("Tokenization:")

    print(
        tokenize(
            "9876543210"
        )
    )

    # --------------------------------------------------------
    # Data minimization
    # --------------------------------------------------------

    customer = {
        "customer_id": 1,
        "name": "Arjun Sharma",
        "email": "arjun@example.com",
        "phone": "9876543210",
        "monthly_income": 50000,
        "monthly_spending": 30000,
        "savings_rate": 0.20,
        "financial_health": 75,
        "financial_stress": 25,
    }

    minimized = minimize_customer_data(
        customer,
        "financial_advice",
    )

    print()
    print("Data Minimization:")
    print(minimized)

    # --------------------------------------------------------
    # Consent
    # --------------------------------------------------------

    consent_manager.grant_consent(
        customer_id=1,
        purposes=[
            "financial_advice",
            "loan_recommendation",
        ],
    )

    print()
    print("Consent:")

    print(
        consent_manager.has_consent(
            customer_id=1,
            purpose="financial_advice",
        )
    )

    print(
        consent_manager.has_consent(
            customer_id=1,
            purpose="fraud_detection",
        )
    )

    print()
    print("========================================")
    print("         PRIVACY TEST COMPLETE")
    print("========================================")
    print()


if __name__ == "__main__":
    main()