"""
Interaction Service

Handles user interactions and updates user preferences.
"""

from config.interaction_weights import INTERACTION_WEIGHTS

from database.repositories.article_repository import ArticleRepository
from database.repositories.interaction_repository import InteractionRepository
from database.repositories.preference_repository import PreferenceRepository


def log_interaction(
    user_id: int,
    article_id: int,
    interaction_type: str
):
    """
    Logs a user interaction and updates preference scores.

    Parameters
    ----------
    user_id : int
    article_id : int
    interaction_type : str
        view | like | bookmark
    """

    # ----------------------------------------
    # Validate interaction type
    # ----------------------------------------

    if interaction_type not in INTERACTION_WEIGHTS:
        raise ValueError(
            f"Invalid interaction type: {interaction_type}"
        )

    # ----------------------------------------
    # Save interaction
    # ----------------------------------------

    InteractionRepository.log_interaction(
        user_id=user_id,
        article_id=article_id,
        interaction_type=interaction_type
    )

    # ----------------------------------------
    # Get article cluster
    # ----------------------------------------

    cluster_name = ArticleRepository.get_cluster_name(
        article_id
    )

    if cluster_name is None:
        return

    # ----------------------------------------
    # Update preference score
    # ----------------------------------------

    PreferenceRepository.increment_preference(
        user_id=user_id,
        cluster_name=cluster_name,
        score=INTERACTION_WEIGHTS[interaction_type]
    )