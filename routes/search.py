"""
Search Routes
"""

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from services.search_services.search_service import (
    search_articles
)

search_bp = Blueprint(
    "search",
    __name__
)


@search_bp.route("/search", methods=["GET"])
def search():

    # User must be logged in
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    # Get query from URL
    query = request.args.get("q", "").strip()

    articles = []

    if query:
        articles = search_articles(query)

    return render_template(
        "search.html",
        query=query,
        articles=articles
    )