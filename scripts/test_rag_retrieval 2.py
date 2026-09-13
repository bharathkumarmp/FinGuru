from app.rag.retriever import retrieve, build_context


print("=" * 60)
print("FINGURU RAG RETRIEVAL TEST")
print("=" * 60)


queries = [
    "Can I take a personal loan if my monthly cash flow is negative?",
    "What should I do if I see a suspicious transaction?",
    "What is an emergency fund?",
    "What information should be protected during KYC?",
]


for query in queries:

    print("\n" + "-" * 60)
    print("QUERY:")
    print(query)

    results = retrieve(
        query=query,
        top_k=3,
    )

    print("\nRETRIEVED DOCUMENTS:")

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        print(
            f"\n[{index}] "
            f"{metadata.get('source', 'unknown')}"
        )

        print(
            "Distance:",
            round(
                result.get(
                    "distance",
                    0.0,
                ),
                4,
            ),
        )

        print(
            result.get(
                "text",
                "",
            )
        )

    print("\nCONTEXT:")
    print(
        build_context(results)
    )


print("\n" + "=" * 60)
print("RAG RETRIEVAL TEST COMPLETE")
print("=" * 60)