"""
AI Assistant Routes

Author: Aayush
"""

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from services.assistant_services.assistant_service import (
    assistant_service
)

assistant_bp = Blueprint(
    "assistant",
    __name__
)


@assistant_bp.route(
    "/assistant",
    methods=["GET", "POST"]
)
def assistant():
    """
    AI Assistant page.
    """

    # ------------------------------------------
    # Authentication
    # ------------------------------------------

    if "user_id" not in session:
        return redirect(
            url_for("auth.login")
        )

    question = ""

    answer = None

    articles = []

    success = True

    # ------------------------------------------
    # Handle Question
    # ------------------------------------------

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).strip()

        result = assistant_service.ask(
            question
        )

        success = result["success"]

        answer = result["answer"]

        articles = result["articles"]

    # ------------------------------------------
    # Render Page
    # ------------------------------------------

    return render_template(
        "assistant.html",
        question=question,
        answer=answer,
        articles=articles,
        success=success
    )