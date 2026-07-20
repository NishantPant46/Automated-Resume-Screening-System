from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from app.services.job_service import create_job
from app.services.job_service import get_all_jobs

job_bp = Blueprint("job", __name__)


@job_bp.route("/jobs")
def jobs():

    jobs = get_all_jobs()

    return render_template(
        "jobs/jobs_list.html",
        jobs=jobs
    )


@job_bp.route("/create-job", methods=["GET", "POST"])
def create_job_page():

    if request.method == "POST":

        create_job(

            request.form["title"],

            request.form["company"],

            request.form["description"],

            request.form["skills"],

            request.form["experience"]

        )

        return redirect(url_for("job.jobs"))

    return render_template("jobs/jobs_create.html")