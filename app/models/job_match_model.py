from app import db


class JobMatch(db.Model):

    __tablename__ = "job_matches"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    resume_id = db.Column(
        db.Integer,
        db.ForeignKey("resumes.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("jobs.id"),
        nullable=False
    )

    similarity_score = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    resume = db.relationship(
        "Resume",
        backref="job_matches"
    )

    job = db.relationship(
        "Job",
        backref="job_matches"
    )

    def __repr__(self):

        return (
            f"<JobMatch Resume {self.resume_id} "
            f"- Job {self.job_id}>"
        )