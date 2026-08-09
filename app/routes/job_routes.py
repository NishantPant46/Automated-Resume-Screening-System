from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from app.services.job_service import create_job
from app.services.job_service import get_all_jobs

from app.models.job_model import Job
from app.models.resume_model import Resume

from app.services.job_match_service import calculate_final_score
from app.services.job_match_service import save_job_match
from app.services.job_match_service import get_matches_for_job
from app.services.job_match_service import match_all_resumes_to_job
from app.services.job_match_service import get_skill_details
from app.services.job_match_service import get_match_status




job_bp = Blueprint(
    "job",
    __name__
)


# ---------------------------------------------
# Jobs List
# ---------------------------------------------

@job_bp.route("/jobs")
def jobs():

    jobs = get_all_jobs()

    return render_template(
        "jobs/jobs_list.html",
        jobs=jobs
    )


# ---------------------------------------------
# Create Job
# ---------------------------------------------

@job_bp.route(
    "/create-job",
    methods=["GET", "POST"]
)
def create_job_page():

    if request.method == "POST":

        title = request.form["title"]
        company = request.form["company"]
        description = request.form["description"]
        skills = request.form["skills"]
        experience = request.form["experience"]
        deadline = request.form["deadline"]

        job = create_job(
            title,
            company,
            description,
            skills,
            experience,
            deadline
        )

        if job is None:

            flash(
                "This job already exists for the selected deadline.",
                "danger"
            )

            return redirect(
                url_for("job.create_job_page")
            )

        flash(
            "Job created successfully.",
            "success"
        )

        return redirect(
            url_for("job.jobs")
        )

    return render_template(
        "jobs/jobs_create.html"
    )


# ---------------------------------------------
# View Job Details
# ---------------------------------------------

@job_bp.route("/job/<int:job_id>")
def view_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    resumes = Resume.query.order_by(
        Resume.upload_date.desc()
    ).all()

    return render_template(
        "jobs/job_detail.html",
        job=job,
        resumes=resumes
    )


# ---------------------------------------------
# Match Single Resume To Job
# ---------------------------------------------

@job_bp.route(
    "/job/<int:job_id>/match",
    methods=["POST"]
)
def match_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    resume_id = request.form.get(
        "resume_id"
    )

    if not resume_id:

        flash(
            "Please select a resume.",
            "danger"
        )

        return redirect(
            url_for(
                "job.view_job",
                job_id=job_id
            )
        )

    resume = Resume.query.get_or_404(
        resume_id
    )

    similarity_score = calculate_final_score(
        resume.processed_text,
        resume.extracted_text,
        job.description,
        job.skills,
        job.experience
    )

    save_job_match(
        resume.id,
        job.id,
        similarity_score
    )

    flash(
        f"Resume matched successfully. "
        f"Similarity Score: {similarity_score}%",
        "success"
    )

    return redirect(
        url_for(
            "job.view_job",
            job_id=job_id
        )
    )


# ---------------------------------------------
# View Job Matches
# ---------------------------------------------

@job_bp.route(
    "/job/<int:job_id>/matches"
)
def job_matches(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    matches = get_matches_for_job(
        job_id
    )

    match_details = []

    for match in matches:

        resume = Resume.query.get(
            match.resume_id
        )

        if not resume:
            continue

        skill_details = get_skill_details(
            resume.processed_text,
            job.skills
        )

        match_details.append({
            "match": match,
            "resume": resume,
            "matched_skills": skill_details[
                "matched_skills"
            ],
            "missing_skills": skill_details[
                "missing_skills"
            ],
            "match_status": get_match_status(
                match.similarity_score
            )
        })

    return render_template(
        "jobs/job_matches.html",
        job=job,
        match_details=match_details
    )


# ---------------------------------------------
# Match All Resumes To Job
# ---------------------------------------------

@job_bp.route(
    "/job/<int:job_id>/match-all",
    methods=["POST"]
)
def match_all_job(job_id):

    job = Job.query.get_or_404(
        job_id
    )

    matches = match_all_resumes_to_job(
        job_id
    )

    if not matches:

        flash(
            "No resumes are available for matching.",
            "warning"
        )

        return redirect(
            url_for(
                "job.view_job",
                job_id=job_id
            )
        )

    flash(
        f"{len(matches)} resumes matched successfully.",
        "success"
    )

    return redirect(
        url_for(
            "job.job_matches",
            job_id=job_id
        )
    )