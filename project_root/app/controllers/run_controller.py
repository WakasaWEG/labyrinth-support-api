from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.middleware.validators import validate_run_finish_payload
from app.services.run_service import start_run, finish_run, RunServiceError


@jwt_required()
def run_start():
    try:
        user_id = int(get_jwt_identity())
        result = start_run(user_id)

        return jsonify({
            "ok": True,
            "data": result
        }), 201

    except RunServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code


@jwt_required()
def run_finish():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json(silent=True) or {}

        is_valid, error_message = validate_run_finish_payload(data)
        if not is_valid:
            return jsonify({
                "ok": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": error_message
                }
            }), 400

        run_id = data.get("runId")
        is_success = data.get("isSuccess")
        rooms_visited = data.get("roomsVisited", 0)
        loot_value = data.get("lootValue", 0)
        duration_seconds = data.get("durationSeconds", 0)

        result = finish_run(
            user_id=user_id,
            run_id=int(run_id),
            is_success=bool(is_success),
            rooms_visited=int(rooms_visited),
            loot_value=int(loot_value),
            duration_seconds=int(duration_seconds)
        )

        return jsonify({
            "ok": True,
            "data": result
        }), 200

    except RunServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code