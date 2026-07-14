from flask import Blueprint

resume_bp = Blueprint("resume", __name__)

@resume_bp.route("/")
def home():
    return "Welcome to Automated Resume Screening System"
