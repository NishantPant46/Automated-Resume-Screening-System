from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash

from app.services.job_service import create_job
from app.services.job_service import get_all_jobs
from app.models.job_model import Job


job_bp = Blueprint(
    "job",
    __name__
)


# ---------------------------------
# Jobs List
# ---------------------------------

@job_bp.route("/jobs")
def jobs():

    jobs = get_all_jobs()

    return render_template(
        "jobs/jobs_list.html",
        jobs=jobs
    )


# ---------------------------------
# Create Job
# ---------------------------------

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


# ---------------------------------
# View Job Details
# ---------------------------------

@job_bp.route("/job/<int:job_id>")
def view_job(job_id):

    job = Job.query.get_or_404(job_id)

    return render_template(
        "jobs/job_detail.html",
        job=job
    )