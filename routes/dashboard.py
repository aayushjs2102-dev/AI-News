from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from services.recommendation_services.recommendation_engine import (
    get_recommendations
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def home():

    return render_template(
        "index.html"
    )


@dashboard_bp.route("/dashboard")
def dashboard():

    if not session.get("is_authenticated"):
        return redirect(
            url_for("auth.login")
        )

    articles = get_recommendations(
        user_id=session["user_id"],
        limit=20
    )

    return render_template(
        "dashboard.html",
        articles=articles
    )