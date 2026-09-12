from typing import Dict, List

from app.rag.pipeline import retrieve_context


def retrieve(
    query: str,
    top_k: int = 5,
) -> List[Dict]:

    if not query.strip():
        return []

    return retrieve_context(
        query=query,
        top_k=top_k,
    )


def build_context(
    results: List[Dict],
) -> str:

    if not results:
        return (
            "No relevant banking knowledge was found."
        )

    context_parts = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        source = metadata.get(
            "source",
            "unknown",
        )

        text = result.get(
            "text",
            "",
        )

        context_parts.append(
            f"[Source {index}: {source}]\n{text}"
        )

    return "\n\n".join(
        context_parts
    )