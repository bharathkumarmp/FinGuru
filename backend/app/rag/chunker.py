from typing import Dict, List


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[str]:
    """
    Split text into overlapping word-based chunks.
    """

    if not text:
        return []

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words),
        )

        chunk = " ".join(
            words[start:end]
        )

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def chunk_documents(
    documents: List[Dict[str, str]],
    chunk_size: int = 500,
    overlap: int = 100,
) -> List[Dict[str, str]]:
    """
    Chunk loaded documents while preserving metadata.
    """

    chunks = []

    for document in documents:

        text_chunks = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, chunk in enumerate(
            text_chunks
        ):

            chunks.append(
                {
                    "text": chunk,
                    "source": document["source"],
                    "category": document["category"],
                    "chunk_id": str(index),
                }
            )

    return chunks