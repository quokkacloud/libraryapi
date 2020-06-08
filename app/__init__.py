from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from .config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    """
        Create application
    """
    app = Flask(__name__)
    app.config.from_object(Config())
    db.init_app(app)
    migrate.init_app(app, db)
    from app.endpoints import register_blueprints
    register_blueprints(app)

    return app
