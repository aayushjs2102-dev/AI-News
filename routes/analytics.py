"""
Analytics Routes

Author: Aayush
"""

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from services.analytics_services.analytics_service import (
    analytics_service
)

analytics_bp = Blueprint(
    "analytics",
    __name__
)


@analytics_bp.route("/analytics")
def analytics():
    """
    Analytics Dashboard
    """

    # ------------------------------------------
    # Authentication
    # ------------------------------------------

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    # ------------------------------------------
    # Load Dashboard Data
    # ------------------------------------------

    dashboard = analytics_service.get_dashboard_data()

    # ------------------------------------------
    # Render Template
    # ------------------------------------------

    return render_template(
        "analytics.html",
        total_users=dashboard["total_users"],
        total_articles=dashboard["total_articles"],
        articles_today=dashboard["articles_today"],
        total_likes=dashboard["total_likes"],
        total_bookmarks=dashboard["total_bookmarks"],
        top_clusters=dashboard["top_clusters"],
        top_sources=dashboard["top_sources"],
        recent_interactions=dashboard["recent_interactions"]
    )