from flask import Blueprint

from app.controllers.run_controller import run_start, run_finish

run_bp = Blueprint("run", __name__)


@run_bp.route("/start", methods=["POST"])
def run_start_route():
    return run_start()


@run_bp.route("/finish", methods=["POST"])
def run_finish_route():
    return run_finish()