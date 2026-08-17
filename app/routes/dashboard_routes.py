from flask import Blueprint
from flask import render_template

from flask_login import login_required

from app.models.resume_model import Resume
from app.models.job_model import Job
from app.models.job_match_model import JobMatch

from app.services.job_match_service import get_selection_status


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    # ---------------------------------
    # Total Jobs
    # ---------------------------------

    total_jobs = Job.query.count()


    # ---------------------------------
    # Total Candidates
    # ---------------------------------

    total_resumes = Resume.query.count()


    # ---------------------------------
    # Recent Candidates
    # ---------------------------------

    recent_candidates = Resume.query.order_by(
        Resume.id.desc()
    ).limit(5).all()


    # ---------------------------------
    # Selected Candidates
    # ---------------------------------

    all_matches = JobMatch.query.all()

    selected_count = 0

    for match in all_matches:

        selection = get_selection_status(
            match.similarity_score
        )

        if selection == "Selected":

            selected_count += 1


    # ---------------------------------
    # Render Dashboard
    # ---------------------------------

    return render_template(
        "dashboard/dashboard.html",
        total_jobs=total_jobs,
        total_resumes=total_resumes,
        recent_candidates=recent_candidates,
        selected_count=selected_count
    )