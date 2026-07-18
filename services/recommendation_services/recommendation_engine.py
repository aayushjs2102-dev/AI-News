"""
Recommendation Engine
"""

from database.repositories.article_repository import (
    ArticleRepository
)

from database.repositories.preference_repository import (
    PreferenceRepository
)

from services.recommendation_services.scorer import (
    score_articles
)


TOP_CLUSTERS = 3


def get_recommendations(
    user_id: int,
    limit: int = 20
):
    """
    Returns personalized recommendations.
    """

    preferences = PreferenceRepository.get_preferences(
        user_id
    )

    # Cold Start

    if not preferences:

        return ArticleRepository.get_trending_articles(
            limit
        )

    clusters = [

        row["cluster_name"]

        for row in preferences[:TOP_CLUSTERS]

    ]

    candidates = ArticleRepository.get_candidate_articles(

        clusters,

        limit * 3

    )

    ranked_articles = score_articles(
        candidates
    )

    return ranked_articles[:limit]