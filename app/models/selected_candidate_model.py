from app import db


class SelectedCandidate(db.Model):

    __tablename__ = "selected_candidates"

    # Prevent the same resume from being selected
    # for the same job more than once.
    __table_args__ = (
        db.UniqueConstraint(
            "resume_id",
            "job_id",
            name="uq_selected_resume_job"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Selected candidate's resume
    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resumes.id"),
        nullable=False
    )

    # Job for which the candidate was selected
    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    # Date and time when candidate was selected
    selected_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False
    )

    # Relationship with Resume
    resume = db.relationship(
        "Resume",
        backref="selected_candidates"
    )

    # Relationship with Job
    job = db.relationship(
        "Job",
        backref="selected_candidates"
    )

    def __repr__(self):

        return (
            f"<SelectedCandidate "
            f"Resume {self.resume_id} "
            f"- Job {self.job_id}>"
        )