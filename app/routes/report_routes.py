from flask import Blueprint
from flask import render_template

from app.models.job_match_model import JobMatch
from app.models.resume_model import Resume
from app.models.job_model import Job

from app.services.job_match_service import get_skill_details
from app.services.job_match_service import get_match_status
from app.services.job_match_service import get_selection_status


report_bp = Blueprint(
    "report",
    __name__
)


# ---------------------------------------------
# Evaluation Reports
# ---------------------------------------------

@report_bp.route("/reports")
def reports():

    matches = JobMatch.query.order_by(
        JobMatch.similarity_score.desc()
    ).all()

    print("===================================")
    print("TOTAL JOB MATCHES:", len(matches))
    print("===================================")

    report_details = []

    for match in matches:

        print(
            "Processing Match:",
            match.id,
            "Resume:",
            match.resume_id,
            "Job:",
            match.job_id,
            "Score:",
            match.similarity_score
        )

        resume = Resume.query.get(
            match.resume_id
        )

        job = Job.query.get(
            match.job_id
        )

        if not resume:
            print(
                "Resume not found:",
                match.resume_id
            )
            continue

        if not job:
            print(
                "Job not found:",
                match.job_id
            )
            continue

        skill_details = get_skill_details(
            resume.processed_text,
            job.skills
        )

        report_details.append({
    "match": match,
    "resume": resume,
    "job": job,

    "matched_skills": skill_details[
        "matched_skills"
    ],

    "missing_skills": skill_details[
        "missing_skills"
    ],

    "status": get_match_status(
        match.similarity_score
    ),

    "selection": get_selection_status(
        match.similarity_score
    )
})

    print(
        "FINAL REPORT DETAILS:",
        len(report_details)
    )

    return render_template(
        "reports/reports.html",
        report_details=report_details
    )