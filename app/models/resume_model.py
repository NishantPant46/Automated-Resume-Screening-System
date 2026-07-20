from app import db

class Resume(db.Model):

    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), nullable=False)

    phone = db.Column(db.String(20))

    file_name = db.Column(db.String(255), nullable=False)

    extracted_text = db.Column(db.Text)   

    processed_text = db.Column(db.Text)

    upload_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )