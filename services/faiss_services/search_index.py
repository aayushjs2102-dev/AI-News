"""
Semantic Search using FAISS

Author: Aayush
"""

import numpy as np

from config.config import Config

from database.repositories.article_repository import (
    ArticleRepository
)

from services.faiss_services.embedding_model import (
    EmbeddingModel
)

from services.faiss_services.faiss_utils import (
    load_index,
    load_mappings
)


class FaissSearcher:

    _instance = None

    _index = None

    _vector_to_article = None

    _article_to_vector = None

    _model = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if self._index is not None:
            return

        print("Loading FAISS index...")

        self._index = load_index()

        (
            self._vector_to_article,
            self._article_to_vector
        ) = load_mappings()

        self._model = EmbeddingModel()

        print("FAISS index loaded.")

    # ----------------------------------------------------------
    # Internal Helpers
    # ----------------------------------------------------------

    @staticmethod
    def _rerank_articles(
        articles,
        predicted_cluster
    ):
        """
        Move articles belonging to the predicted cluster
        to the front while preserving FAISS order.
        """

        if predicted_cluster is None:
            return articles

        preferred = []
        remaining = []

        for article in articles:

            if article.get("cluster_name") == predicted_cluster:
                preferred.append(article)
            else:
                remaining.append(article)

        return preferred + remaining

    # ----------------------------------------------------------
    # Core Retrieval Method
    # ----------------------------------------------------------

    def retrieve(
        self,
        query_vector: np.ndarray,
        k: int = None,
        predicted_cluster: str = None
    ):
        """
        Performs semantic retrieval using FAISS and
        optionally reranks the results using the
        predicted query cluster.
        """

        if k is None:
            k = Config.RAG_TOP_K

        search_k = max(
            Config.RAG_INITIAL_SEARCH_K,
            k
        )

        distances, indices = self._index.search(
            query_vector.reshape(1, -1),
            search_k
        )

        article_ids = []

        similarity_scores = {}

        for score, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx == -1:
                continue

            if score < Config.RAG_MIN_SIMILARITY:
                continue

            article_id = self._vector_to_article[idx]

            article_ids.append(article_id)

            similarity_scores[article_id] = float(score)

        if not article_ids:
            return []

        articles = ArticleRepository.get_articles_by_ids(
            article_ids
        )

        for article in articles:

            article["similarity_score"] = similarity_scores.get(
                article["id"],
                0.0
            )

        articles = self._rerank_articles(
            articles,
            predicted_cluster
        )

        return articles[:k]

    # ----------------------------------------------------------
    # Search
    # ----------------------------------------------------------

    def search(
        self,
        query: str,
        k: int = None,
        predicted_cluster: str = None
    ):

        if k is None:
            k = Config.RAG_TOP_K

        query_vector = self._model.encode(query)

        return self.retrieve(
            query_vector=query_vector,
            k=k,
            predicted_cluster=predicted_cluster
        )

    # ----------------------------------------------------------
    # Similar Articles
    # ----------------------------------------------------------

    def similar_articles(
        self,
        article_id: int,
        k: int = 6
    ):

        article = ArticleRepository.get_article_by_id(
            article_id
        )

        if article is None:
            return []

        text = (
            article["title"]
            + "\n"
            + article["summary"]
        )

        query_vector = self._model.encode(
            text
        )

        articles = self.retrieve(
            query_vector=query_vector,
            k=k + 1,
            predicted_cluster=article.get(
                "cluster_name"
            )
        )

        filtered = []

        for candidate in articles:

            if candidate["id"] == article_id:
                continue

            filtered.append(candidate)

            if len(filtered) == k:
                break

        return filtered