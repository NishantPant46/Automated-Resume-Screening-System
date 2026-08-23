from app import db


class Job(db.Model):

    __tablename__ = "jobs"

    __table_args__ = (
        db.UniqueConstraint(
            "title",
            "company",
            "deadline",
            name="unique_job_posting"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    recruiter_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )

    company = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    processed_description = db.Column(
        db.Text
    )

    skills = db.Column(
        db.Text
    )

    experience = db.Column(
        db.Integer
    )

    deadline = db.Column(
        db.Date,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    # Recruiter relationship
    recruiter = db.relationship(
        "User",
        back_populates="jobs"
    )

    def __repr__(self):

        return (
            f"<Job {self.title} "
            f"- {self.company}>"
        )