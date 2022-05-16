import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .exceptions import register_error_handler
from .context import Context


db = SQLAlchemy()

def init_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']

    db.init_app(app)

    with app.app_context():
        from .models import HiredEmployees, Departments, Jobs
        db.create_all()

        register_error_handler(app)

        from .routes import bp
        app.register_blueprint(bp)

        return app

def get_context():
    return Context(db.session)