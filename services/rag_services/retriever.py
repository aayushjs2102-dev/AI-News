"""
RAG Retriever

Author: Aayush
"""

from config.config import Config

from services.classification_services.classifier import (
    ZeroShotClassifier
)

from services.faiss_services.embedding_model import (
    EmbeddingModel
)

from services.faiss_services.search_index import (
    FaissSearcher
)

from utils.logger import get_logger

logger = get_logger()


class Retriever:
    """
    Retrieves the most relevant news articles for a user question.

    Workflow
    --------
    1. Classify the user's question using the zero-shot classifier.
    2. Generate the embedding for the question.
    3. Perform FAISS semantic search.
    4. Rerank the semantic results using the predicted cluster.
    5. Return the best matching articles.
    """

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.searcher = FaissSearcher()

        self.classifier = ZeroShotClassifier()

    def retrieve(
        self,
        question: str,
        top_k: int = None
    ):
        """
        Retrieve the most relevant articles for a user query.

        Parameters
        ----------
        question : str
            User's natural language query.

        top_k : int, optional
            Number of articles to return.

        Returns
        -------
        list[dict]
            Ranked articles.
        """

        if top_k is None:
            top_k = Config.RAG_TOP_K

        # --------------------------------------------------
        # Predict query cluster
        # --------------------------------------------------

        predicted_cluster = None

        try:

            result = self.classifier.classify(question)

            if (
                result["score"]
                >= Config.RAG_CLASSIFICATION_THRESHOLD
            ):

                predicted_cluster = result["cluster"]

                logger.info(
                    f"Query classified as "
                    f"'{predicted_cluster}' "
                    f"(confidence={result['score']:.3f})"
                )

            else:

                logger.info(
                    f"Low classification confidence "
                    f"({result['score']:.3f}). "
                    f"Using semantic search only."
                )

        except Exception as e:

            logger.warning(
                f"Query classification failed: {e}"
            )

        # --------------------------------------------------
        # Semantic Retrieval
        # --------------------------------------------------

        query_vector = self.embedding_model.encode(
            question
        )

        articles = self.searcher.retrieve(
            query_vector=query_vector,
            k=top_k,
            predicted_cluster=predicted_cluster
        )

        logger.info(
            f"Retrieved {len(articles)} article(s)."
        )

        return articles