from flask import Blueprint

from app.controllers.profile_controller import profile

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/", methods=["GET"])
def profile_route():
    return profile()