"""
Search Service

Handles business logic for searching news articles.
"""

from database.repositories.article_repository import (
    ArticleRepository
)

from services.faiss_services.search_index import (
    FaissSearcher
)


# ----------------------------------------------------------
# Singleton FAISS Searcher
# ----------------------------------------------------------

_searcher = FaissSearcher()


# ----------------------------------------------------------
# Search Articles
# ----------------------------------------------------------

def search_articles(
    query: str,
    limit: int = 20
):
    """
    Search articles using FAISS semantic search.

    Parameters
    ----------
    query : str

    limit : int

    Returns
    -------
    list[dict]
    """

    query = query.strip()

    if not query:
        return []

    return _searcher.search(
        query=query,
        k=limit
    )