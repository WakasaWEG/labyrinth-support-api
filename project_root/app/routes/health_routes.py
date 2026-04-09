from flask import Blueprint

from app.controllers.health_controller import health_check, db_check

health_bp = Blueprint("health", __name__)


@health_bp.route("/", methods=["GET"])
def health_route():
    return health_check()


@health_bp.route("/db", methods=["GET"])
def db_route():
    return db_check()