from flask import Blueprint
from flask import render_template

from flask_login import login_required

from app.models.job_match_model import JobMatch
from app.models.resume_model import Resume
from app.models.job_model import Job


selected_bp = Blueprint(
    "selected",
    __name__
)


# ---------------------------------------------
# Selected Candidates
# ---------------------------------------------

@selected_bp.route("/selected")
@login_required
def selected_candidates():

    matches = JobMatch.query.filter(
        JobMatch.similarity_score >= 50
    ).order_by(
        JobMatch.similarity_score.desc()
    ).all()

    selected_candidates = []

    for match in matches:

        resume = Resume.query.get(
            match.resume_id
        )

        job = Job.query.get(
            match.job_id
        )

        if not resume:
            continue

        if not job:
            continue

        selected_candidates.append({

            "resume": resume,

            "job": job
        })

    return render_template(
        "selected/selected_candidates.html",
        selected_candidates=selected_candidates
    )