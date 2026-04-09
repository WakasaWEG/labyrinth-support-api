from flask import Blueprint

from app.controllers.leaderboard_controller import leaderboard

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/", methods=["GET"])
def leaderboard_route():
    return leaderboard()