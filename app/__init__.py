from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.resume_routes import resume_bp

    app.register_blueprint(resume_bp)

    return app