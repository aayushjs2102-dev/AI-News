from flask import (
    Blueprint,
    redirect,
    session,
    url_for
)

from flask import request

from database.repositories.article_repository import (
    ArticleRepository
)

from services.interaction_services.interaction import (
    log_interaction
)



article_bp = Blueprint(
    "article",
    __name__
)


@article_bp.route("/article/<int:article_id>/like", methods=["POST"])
def like_article(article_id):

    if not session.get("is_authenticated"):
        return redirect(url_for("auth.login"))

    log_interaction(
        user_id=session["user_id"],
        article_id=article_id,
        interaction_type="like"
    )

    return redirect(url_for("dashboard.dashboard"))


@article_bp.route("/article/<int:article_id>/bookmark", methods=["POST"])
def bookmark_article(article_id):

    if not session.get("is_authenticated"):
        return redirect(url_for("auth.login"))

    log_interaction(
        user_id=session["user_id"],
        article_id=article_id,
        interaction_type="bookmark"
    )

    return redirect(url_for("dashboard.dashboard"))

@article_bp.route("/article/<int:article_id>")
def open_article(article_id):

    if not session.get("is_authenticated"):
        return redirect(
            url_for("auth.login")
        )

    article = ArticleRepository.get_article_by_id(
        article_id
    )

    if article is None:
        return "Article not found", 404

    log_interaction(
        user_id=session["user_id"],
        article_id=article_id,
        interaction_type="view"
    )

    return redirect(
        article["url"]
    )