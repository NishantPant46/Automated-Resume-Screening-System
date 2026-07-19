from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.models.resume_model import Resume

    from app.routes.resume_routes import resume_bp

    app.register_blueprint(resume_bp)

    from app.routes.report_routes import report_bp

    app.register_blueprint(report_bp)

    return app