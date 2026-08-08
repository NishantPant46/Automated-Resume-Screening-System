from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)

    # Import models
    from app.models.resume_model import Resume
    from app.models.job_model import Job
    from app.models.job_match_model import JobMatch

    # Import routes
    from app.routes.resume_routes import resume_bp
    from app.routes.report_routes import report_bp
    from app.routes.job_routes import job_bp
    from app.routes.dashboard_routes import dashboard_bp

    # Register blueprints
    app.register_blueprint(resume_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(job_bp)
    app.register_blueprint(dashboard_bp)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app