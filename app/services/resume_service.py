from app import db
from app.models.resume_model import Resume


def save_resume_data(
    full_name,
    email,
    phone,
    file_name,
    extracted_text,
    processed_text
):

    resume = Resume(

        full_name=full_name,

        email=email,

        phone=phone,

        file_name=file_name,

        extracted_text=extracted_text,

        processed_text=processed_text

    )

    db.session.add(resume)
    db.session.commit()

    return resume


def get_all_resumes():
    return Resume.query.all()