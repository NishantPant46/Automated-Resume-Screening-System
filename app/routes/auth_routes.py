from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user
)

from werkzeug.security import check_password_hash

from app.models.user_model import User


auth_bp = Blueprint(
    "auth",
    __name__
)


# ---------------------------------
# Login
# ---------------------------------

@auth_bp.route(
    "/",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(
            email=email
        ).first()

        if user is None:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "auth/login.html"
            )

        if not check_password_hash(
            user.password,
            password
        ):

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "auth/login.html"
            )

        # Login user
        login_user(
            user,
            remember=remember
        )

        # ---------------------------------
        # Redirect according to role
        # ---------------------------------

        if user.role == "recruiter":

            return redirect(
                url_for("dashboard.dashboard")
            )

        return redirect(
            url_for("resume.resume_page")
        )

    # IMPORTANT:
    # This handles normal GET requests.
    return render_template(
        "auth/login.html"
    )


# ---------------------------------
# Logout
# ---------------------------------

@auth_bp.route("/logout")
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )