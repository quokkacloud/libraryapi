from .authors import authors_blueprint
from .books import books_blueprint


def register_blueprints(app):
    """
        Register all blueprints
    """
    app.register_blueprint(authors_blueprint)
    app.register_blueprint(books_blueprint)
