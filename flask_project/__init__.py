from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_project.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Start project to Flask."""

    print(__name__)
    app = Flask(__name__)
    login_manager.init_app(app)

    from flask_project.main.routes import main
    app.register_blueprint(main)

    app.config.from_object(Config)

    return app
