from app import db


class Job(db.Model):

    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    company = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=False)

    processed_description = db.Column(db.Text)

    skills = db.Column(db.Text)

    experience = db.Column(db.Integer)

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):
        return f"<Job {self.title}>"