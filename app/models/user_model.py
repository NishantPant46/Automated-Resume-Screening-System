from app import db
from flask_login import UserMixin


class User(
    UserMixin,
    db.Model
):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="candidate"
    )

    # Candidate -> Resume
    resumes = db.relationship(
        "Resume",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )

    # Recruiter -> Job
    jobs = db.relationship(
        "Job",
        back_populates="recruiter",
        cascade="all, delete-orphan"
    )

    def __repr__(self):

        return (
            f"<User {self.email} "
            f"- {self.role}>"
        )