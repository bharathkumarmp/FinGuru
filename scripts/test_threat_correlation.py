from app.services.threat_correlation import correlate_security_signals


def run_test(
    name,
    fraud,
    ueba,
    identity,
):
    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = correlate_security_signals(
        fraud_score=fraud,
        ueba_score=ueba,
        identity_risk_score=identity,
    )

    print("\nTHREAT SCORE")
    print(result["threat_score"])

    print("\nTHREAT LEVEL")
    print(result["threat_level"])

    print("\nRECOMMENDED ACTION")
    print(result["recommended_action"])

    print("\nSIGNALS")

    for key, value in result["signal_scores"].items():
        print(f"{key}: {value}")

    print("\nCORRELATION")

    for key, value in result["correlation"].items():
        print(f"{key}: {value}")

    print("\nEVIDENCE")

    for item in result["evidence"]:
        print("-", item)

    print("\nEVIDENCE TIMELINE")

    for item in result["evidence_timeline"]:
        print("-", item)


def main():

    # Normal customer
    run_test(
        "TEST 1 — NORMAL",
        fraud=6,
        ueba=6,
        identity=0,
    )

    # Suspicious transaction
    run_test(
        "TEST 2 — SUSPICIOUS",
        fraud=60,
        ueba=55,
        identity=50,
    )

    # Account takeover scenario
    run_test(
        "TEST 3 — CRITICAL ACCOUNT TAKEOVER",
        fraud=90,
        ueba=85,
        identity=80,
    )

    print("\n" + "=" * 60)
    print("Threat Correlation tests completed.")
    print("=" * 60)


if __name__ == "__main__":
    main()