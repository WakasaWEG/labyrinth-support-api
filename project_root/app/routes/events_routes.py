from flask import Blueprint

from app.controllers.events_controller import create_event, list_events

events_bp = Blueprint("events", __name__)


@events_bp.route("/", methods=["POST"])
def create_event_route():
    return create_event()


@events_bp.route("/", methods=["GET"])
def list_events_route():
    return list_events()