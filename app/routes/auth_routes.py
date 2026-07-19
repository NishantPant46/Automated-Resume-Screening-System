from flask import Blueprint, render_template

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/")
def home():
    return render_template("auth/login.html")
