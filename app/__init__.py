from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

login_manager = LoginManager()


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        "app.config.Config"
    )

    # ---------------------------------
    # Initialize Database
    # ---------------------------------

    db.init_app(app)

    # ---------------------------------
    # Flask Login
    # ---------------------------------

    login_manager.init_app(app)

    login_manager.login_view = "resume.home"

    # ---------------------------------
    # Import Models
    # ---------------------------------

    from app.models.resume_model import Resume
    from app.models.job_model import Job
    from app.models.job_match_model import JobMatch
    from app.models.user_model import User

    # ---------------------------------
    # User Loader
    # ---------------------------------

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            User,
            int(user_id)
        )

    # ---------------------------------
    # Import Routes
    # ---------------------------------

    from app.routes.resume_routes import resume_bp
    from app.routes.job_routes import job_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.selected_routes import selected_bp

    # ---------------------------------
    # Register Blueprints
    # ---------------------------------

    app.register_blueprint(
        resume_bp
    )

    app.register_blueprint(
        job_bp
    )

    app.register_blueprint(
        dashboard_bp
    )

    app.register_blueprint(
        selected_bp
    )

    # ---------------------------------
    # Create Database Tables
    # ---------------------------------

    with app.app_context():

        db.create_all()

    return app