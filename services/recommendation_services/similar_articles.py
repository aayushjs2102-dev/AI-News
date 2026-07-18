"""
Similar Articles Service
"""

from services.faiss_services.search_index import (
    FaissSearcher
)


_searcher = FaissSearcher()


def get_similar_articles(
    article_id: int,
    limit: int = 5
):
    """
    Returns semantically similar articles.
    """

    return _searcher.similar_articles(
        article_id=article_id,
        k=limit + 1
    )