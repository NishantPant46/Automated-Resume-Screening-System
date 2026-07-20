from app import db
from app.models.job_model import Job

from app.services.nlp_service import preprocess_text


def create_job(
        title,
        company,
        description,
        skills,
        experience
):

    processed_description = preprocess_text(description)

    job = Job(

        title=title,

        company=company,

        description=description,

        processed_description=processed_description,

        skills=skills,

        experience=experience

    )

    db.session.add(job)

    db.session.commit()

    return job


def get_all_jobs():

    return Job.query.all()