"""
Recommendation Scorer

Ranks candidate articles.
"""


def score_articles(
    articles: list[dict]
) -> list[dict]:
    """
    Scores and sorts articles.

    Current Version:
        - Freshness only.

    Future:
        - Preference
        - Trending
        - FAISS similarity
    """

    return sorted(

        articles,

        key=lambda article: article["published_at"],

        reverse=True
    )