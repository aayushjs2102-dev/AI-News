"""
Semantic Search using FAISS

Author: Aayush
"""

import os
import pickle

import faiss

from database.repositories.article_repository import ArticleRepository
from services.faiss_services.embedding_model import EmbeddingModel


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

FAISS_DIR = os.path.join(BASE_DIR, "faiss")

INDEX_PATH = os.path.join(
    FAISS_DIR,
    "article_index.faiss"
)

MAPPING_PATH = os.path.join(
    FAISS_DIR,
    "article_mapping.pkl"
)


class FaissSearcher:

    _instance = None
    _index = None
    _mapping = None
    _model = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self._index is not None:
            return

        print("Loading FAISS index...")

        self._index = faiss.read_index(INDEX_PATH)

        with open(MAPPING_PATH, "rb") as file:
            self._mapping = pickle.load(file)

        self._model = EmbeddingModel()

        print("FAISS index loaded.")

    def search(self, query: str, k: int = 10):

        query_vector = self._model.encode(query)

        distances, indices = self._index.search(
            query_vector.reshape(1, -1),
            k
        )

        article_ids = []

        similarity_scores = {}

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            article_id = self._mapping[idx]

            article_ids.append(article_id)

            similarity_scores[article_id] = float(score)

        articles = ArticleRepository.get_articles_by_ids(article_ids)

        for article in articles:

            article["similarity_score"] = similarity_scores.get(
                article["id"],
                0.0
            )

        return articles