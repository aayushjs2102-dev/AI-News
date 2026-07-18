"""
Similar Articles Service
"""

from database.repositories.article_repository import (
    ArticleRepository
)


def get_similar_articles(
    article_id: int,
    limit: int = 5
):
    """
    Returns articles related to the given article.
    """

    return ArticleRepository.get_similar_articles(
        article_id=article_id,
        limit=limit
    )