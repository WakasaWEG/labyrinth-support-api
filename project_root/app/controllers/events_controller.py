from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from app.middleware.auth_jwt import auth_required
from app.middleware.validators import validate_event_payload
from app.services.events_service import post_event, get_user_events, EventsServiceError


@auth_required(roles=["player", "admin"])
def create_event():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json(silent=True) or {}

        is_valid, error_message = validate_event_payload(data)
        if not is_valid:
            return jsonify({
                "ok": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": error_message
                }
            }), 400

        event_type = data.get("eventType")
        run_id = data.get("runId")
        payload = data.get("payload", {})

        result = post_event(
            user_id=user_id,
            run_id=run_id,
            event_type=event_type,
            payload=payload
        )

        return jsonify({
            "ok": True,
            "data": result
        }), 201

    except EventsServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code


@auth_required(roles=["player", "admin"])
def list_events():
    try:
        user_id = int(get_jwt_identity())
        result = get_user_events(user_id)

        return jsonify({
            "ok": True,
            "data": result
        }), 200

    except EventsServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code