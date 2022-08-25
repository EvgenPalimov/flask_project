from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_project.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    """Start project to Flask."""

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from flask_project.main.routes import main
    from flask_project.users.routes import users
    from flask_project.posts.routes import posts
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(users)

    return app
