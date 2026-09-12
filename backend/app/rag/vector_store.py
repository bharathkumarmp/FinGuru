from pathlib import Path
from typing import Dict, List, Optional

import chromadb


BASE_DIR = Path(__file__).resolve().parents[3]

VECTOR_STORE_PATH = (
    BASE_DIR / "vector_store" / "chroma"
)

COLLECTION_NAME = "finguru_knowledge"


class VectorStore:

    def __init__(
        self,
        path: Optional[str] = None,
    ):

        store_path = Path(
            path
            if path
            else VECTOR_STORE_PATH
        )

        store_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.client = chromadb.PersistentClient(
            path=str(store_path)
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={
                    "description": (
                        "FinGuru banking knowledge base"
                    )
                },
            )
        )

    def add_documents(
        self,
        chunks: List[Dict[str, str]],
        embeddings,
    ):

        if not chunks:
            return

        ids = []

        documents = []

        metadatas = []

        embedding_list = []

        for index, chunk in enumerate(
            chunks
        ):

            ids.append(
                f"{chunk['source']}_{chunk['chunk_id']}"
            )

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                {
                    "source": chunk["source"],
                    "category": chunk["category"],
                    "chunk_id": chunk["chunk_id"],
                }
            )

            embedding_list.append(
                embeddings[index].tolist()
            )

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embedding_list,
        )

    def search(
        self,
        query_embedding,
        top_k: int = 5,
    ):

        if self.collection.count() == 0:
            return []

        result = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=top_k,
        )

        documents = (
            result.get("documents", [[]])[0]
        )

        metadatas = (
            result.get("metadatas", [[]])[0]
        )

        distances = (
            result.get("distances", [[]])[0]
        )

        results = []

        for index, document in enumerate(
            documents
        ):

            results.append(
                {
                    "text": document,
                    "metadata": metadatas[index],
                    "distance": distances[index],
                }
            )

        return results