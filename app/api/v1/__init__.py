from flask import Blueprint
from app.api.v1 import image


def create_blueprint_v1() -> Blueprint:
    """
    Create Blueprint for api v1 endpoint
    :return: Blueprint v1
    """
    bp_v1 = Blueprint('v1', __name__)
    image.api.register(bp_v1)
    return bp_v1
