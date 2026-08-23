from app import create_app, db

from app.models.user_model import User

from werkzeug.security import generate_password_hash


app = create_app()


with app.app_context():

    email = "admin@gmail.com"

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:

        print(
            "User already exists."
        )

    else:

        user = User(

            name="System Recruiter",

            email=email,

            password=generate_password_hash(
                "admin123"
            ),

            role="recruiter"
        )

        db.session.add(user)

        db.session.commit()

        print(
            "Recruiter account created successfully."
        )

        print(
            "Email: admin@gmail.com"
        )

        print(
            "Password: admin123"
        )