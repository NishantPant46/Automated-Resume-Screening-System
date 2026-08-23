from datetime import datetime

from flask_login import current_user

from app import db
from app.models.job_model import Job


def create_job(
    title,
    company,
    description,
    skills,
    experience,
    deadline
):

    # Convert deadline from HTML string
    # Example: "2026-08-25"
    # into Python date object
    deadline = datetime.strptime(
        deadline,
        "%Y-%m-%d"
    ).date()

    # Check for duplicate job
    # Same title + company + deadline = duplicate
    existing_job = Job.query.filter_by(
        title=title,
        company=company,
        deadline=deadline
    ).first()

    if existing_job:
        return None

    # Create new job
    job = Job(
        recruiter_id=current_user.id,
        title=title,
        company=company,
        description=description,
        skills=skills,
        experience=int(experience),
        deadline=deadline
    )

    # Save job
    db.session.add(job)
    db.session.commit()

    return job


def get_all_jobs():

    return Job.query.order_by(
        Job.created_at.desc()
    ).all()

