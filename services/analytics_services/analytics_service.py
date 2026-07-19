"""
Analytics Service

Author: Aayush

Provides business logic for the Analytics Dashboard.
"""

from database.repositories.analytics_repository import (
    analytics_repository
)


class AnalyticsService:
    """
    Analytics business layer.
    """

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def get_dashboard_data(self) -> dict:
        """
        Collect all analytics required by the dashboard.
        """

        return {

            # ----------------------------------------
            # KPI Cards
            # ----------------------------------------

            "total_users":
                analytics_repository.get_total_users(),

            "total_articles":
                analytics_repository.get_total_articles(),

            "articles_today":
                analytics_repository.get_articles_today(),

            "total_likes":
                analytics_repository.get_total_likes(),

            "total_bookmarks":
                analytics_repository.get_total_bookmarks(),

            # ----------------------------------------
            # Charts
            # ----------------------------------------

            "top_clusters":
                analytics_repository.get_top_clusters(),

            "top_sources":
                analytics_repository.get_top_sources(),

            # ----------------------------------------
            # Activity
            # ----------------------------------------

            "recent_interactions":
                analytics_repository.get_recent_interactions()

        }


analytics_service = AnalyticsService()