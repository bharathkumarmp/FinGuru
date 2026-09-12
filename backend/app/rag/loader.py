from pathlib import Path
from typing import Dict, List


def load_documents(
    data_directory: str = "rag_data",
) -> List[Dict[str, str]]:
    """
    Load text documents from the RAG knowledge base.

    Each document contains:
        - text
        - source
        - category
    """

    base_path = Path(data_directory)

    if not base_path.exists():
        raise FileNotFoundError(
            f"RAG data directory not found: {data_directory}"
        )

    documents = []

    for file_path in sorted(
        base_path.rglob("*")
    ):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in {
            ".txt",
            ".md",
        }:
            continue

        text = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not text:
            continue

        relative_path = file_path.relative_to(
            base_path
        )

        category = (
            relative_path.parts[0]
            if len(relative_path.parts) > 1
            else "general"
        )

        documents.append(
            {
                "text": text,
                "source": str(relative_path),
                "category": category,
            }
        )

    return documents