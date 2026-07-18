from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from services.auth_services.auth import (
    register_user,
    login_user
)

auth_bp = Blueprint(
    "auth",
    __name__
)


# ----------------------------------------------------------
# Register
# ----------------------------------------------------------

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        success, message = register_user(
            username=username,
            email=email,
            password=password
        )

        flash(
            message,
            "success" if success else "danger"
        )

        if success:
            return redirect(
                url_for("auth.login")
            )

    return render_template(
        "register.html"
    )


# ----------------------------------------------------------
# Login
# ----------------------------------------------------------

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"]

        success, user = login_user(
            username=username,
            password=password
        )

        if success:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(
                url_for("dashboard.dashboard")
            )

        flash(
            "Invalid username or password.",
            "danger"
        )

    return render_template(
        "login.html"
    )


# ----------------------------------------------------------
# Logout
# ----------------------------------------------------------

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("dashboard.home")
    )