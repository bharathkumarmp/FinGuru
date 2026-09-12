from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = MODEL_NAME,
    ):
        self.model_name = model_name

        self.model = SentenceTransformer(
            model_name
        )

    def encode(
        self,
        texts: List[str],
    ) -> np.ndarray:

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )


_embedding_model = None


def get_embedding_model() -> EmbeddingModel:

    global _embedding_model

    if _embedding_model is None:
        _embedding_model = EmbeddingModel()

    return _embedding_model


def generate_embeddings(
    texts: List[str],
) -> np.ndarray:

    if not texts:
        return np.empty(
            (0, 384)
        )

    model = get_embedding_model()

    return model.encode(texts)