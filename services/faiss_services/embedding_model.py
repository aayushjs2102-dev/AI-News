"""
Embedding Model Singleton

Author: Aayush
"""

import torch

from sentence_transformers import SentenceTransformer


MODEL_NAME = "BAAI/bge-small-en-v1.5"


class EmbeddingModel:

    _instance = None

    _model = None

    def __new__(cls):

        if cls._instance is None:

            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self._model is not None:
            return

        if torch.backends.mps.is_available():

            device = "mps"

        elif torch.cuda.is_available():

            device = "cuda"

        else:

            device = "cpu"

        print(f"Loading embedding model on {device}...")

        self._model = SentenceTransformer(
            MODEL_NAME,
            device=device
        )

        print("Embedding model loaded.")

    def encode(self, text):

        return self._model.encode(
            text,
            normalize_embeddings=True
        )