from flask import Blueprint, render_template

from app.models.resume_model import Resume
from app.models.job_model import Job

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():

    total_jobs = Job.query.count()

    total_resumes = Resume.query.count()

    recent_candidates = Resume.query.order_by(
        Resume.id.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/dashboard.html",
        total_jobs=total_jobs,
        total_resumes=total_resumes,
        recent_candidates=recent_candidates
    )