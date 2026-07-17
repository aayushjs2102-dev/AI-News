"""
Recommendation Engine
"""

from database.repositories.article_repository import ArticleRepository
from database.repositories.preference_repository import PreferenceRepository


def get_recommendations(
    user_id: int,
    limit: int = 20
):
    """
    Returns personalized news recommendations.
    """

    preferences = PreferenceRepository.get_preferences(user_id)

    if not preferences:
        return []

    clusters = [
        row["cluster_name"]
        for row in preferences[:3]
    ]

    articles = ArticleRepository.get_articles_by_clusters(
        clusters,
        limit
    )

    return articles