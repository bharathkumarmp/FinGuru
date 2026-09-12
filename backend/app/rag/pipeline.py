from typing import Dict, List

from app.rag.loader import load_documents
from app.rag.chunker import chunk_documents
from app.rag.embeddings import generate_embeddings
from app.rag.vector_store import VectorStore


def build_vector_store(
    data_directory: str = "rag_data",
) -> Dict[str, int]:

    documents = load_documents(
        data_directory
    )

    chunks = chunk_documents(
        documents
    )

    if not chunks:
        return {
            "documents": 0,
            "chunks": 0,
        }

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    vector_store = VectorStore()

    vector_store.add_documents(
        chunks,
        embeddings,
    )

    return {
        "documents": len(documents),
        "chunks": len(chunks),
    }


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> List[Dict]:

    embedding = generate_embeddings(
        [query]
    )[0]

    vector_store = VectorStore()

    return vector_store.search(
        query_embedding=embedding,
        top_k=top_k,
    )