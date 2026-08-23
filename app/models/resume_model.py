from app import db


class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        nullable=False
    )

    phone = db.Column(
        db.String(20)
    )

    file_name = db.Column(
        db.String(255),
        nullable=False
    )

    extracted_text = db.Column(
        db.Text
    )

    processed_text = db.Column(
        db.Text
    )

    predicted_job_role = db.Column(
        db.String(100)
    )

    upload_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Candidate relationship
    candidate = db.relationship(
        "User",
        back_populates="resumes"
    )

    def __repr__(self):

        return (
            f"<Resume {self.id} "
            f"- {self.full_name}>"
        )