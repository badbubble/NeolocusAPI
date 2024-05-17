from flask import Flask
from app.api.v1 import create_blueprint_v1


def register_blueprints(app: Flask) -> None:
    """
    Register all blueprints with the Flask app.
    :param app: Flask application.
    :return:
    """
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def create_app() -> Flask:
    """
    Create the Flask app.
    :return:
    """
    app = Flask(__name__)
    register_blueprints(app)
    return app
