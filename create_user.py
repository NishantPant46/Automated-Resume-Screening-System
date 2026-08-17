from app import create_app, db
from app.models.user_model import User


app = create_app()


with app.app_context():

    user = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if not user:

        user = User(
            email="admin@gmail.com",
            password="admin123"
        )

        db.session.add(user)
        db.session.commit()

        print("User created successfully.")

    else:

        print("User already exists.")