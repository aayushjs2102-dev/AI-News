"""
Search Service

Handles business logic for searching news articles.
"""

from database.repositories.article_repository import (
    ArticleRepository
)


def search_articles(
    query: str,
    limit: int = 20
):
    """
    Search articles.

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

    return ArticleRepository.search_articles(
        query=query,
        limit=limit
    )