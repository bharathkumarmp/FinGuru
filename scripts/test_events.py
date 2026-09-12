from app.events import (
    EventType,
    publish_event,
    process_event,
)


def main():

    print()
    print("========================================")
    print("        FINGURU EVENT SYSTEM TEST")
    print("========================================")

    # --------------------------------------------------------
    # Test 1: Salary event
    # --------------------------------------------------------

    salary_event = publish_event(
        event_type=EventType.SALARY_CREDITED,
        customer_id=1,
        data={
            "amount": 50000,
            "source": "salary",
        },
    )

    print()
    print("SALARY EVENT")
    print(salary_event)

    salary_result = process_event(
        salary_event
    )

    print("HANDLER RESULT")
    print(salary_result)

    # --------------------------------------------------------
    # Test 2: Large transaction
    # --------------------------------------------------------

    transaction_event = publish_event(
        event_type=EventType.LARGE_TRANSACTION,
        customer_id=1,
        data={
            "transaction_id": 1001,
            "amount": 250000,
            "merchant": "Example Merchant",
        },
    )

    print()
    print("LARGE TRANSACTION EVENT")
    print(transaction_event)

    transaction_result = process_event(
        transaction_event
    )

    print("HANDLER RESULT")
    print(transaction_result)

    # --------------------------------------------------------
    # Test 3: New device
    # --------------------------------------------------------

    device_event = publish_event(
        event_type=EventType.NEW_DEVICE,
        customer_id=1,
        data={
            "device_id": "device_new_001",
            "location": "Ahmedabad",
        },
    )

    print()
    print("NEW DEVICE EVENT")
    print(device_event)

    device_result = process_event(
        device_event
    )

    print("HANDLER RESULT")
    print(device_result)

    # --------------------------------------------------------
    # Test 4: Security threat
    # --------------------------------------------------------

    threat_event = publish_event(
        event_type=EventType.SECURITY_THREAT,
        customer_id=1,
        data={
            "threat_score": 90,
            "risk_level": "CRITICAL",
        },
    )

    print()
    print("SECURITY THREAT EVENT")
    print(threat_event)

    threat_result = process_event(
        threat_event
    )

    print("HANDLER RESULT")
    print(threat_result)

    print()
    print("========================================")
    print("        EVENT SYSTEM TEST COMPLETE")
    print("========================================")
    print()


if __name__ == "__main__":
    main()