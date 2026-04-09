from flask import jsonify, request

from app.middleware.validators import validate_register_payload, validate_login_payload
from app.services.auth_service import register_user, login_user, AuthServiceError


def register():
    try:
        data = request.get_json(silent=True) or {}

        is_valid, error_message = validate_register_payload(data)
        if not is_valid:
            return jsonify({
                "ok": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": error_message
                }
            }), 400

        email = data.get("email", "").strip()
        password = data.get("password", "")
        nickname = data.get("nickname", "").strip()

        result = register_user(email=email, password=password, nickname=nickname)

        return jsonify({
            "ok": True,
            "data": result
        }), 201

    except AuthServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code


def login():
    try:
        data = request.get_json(silent=True) or {}

        is_valid, error_message = validate_login_payload(data)
        if not is_valid:
            return jsonify({
                "ok": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": error_message
                }
            }), 400

        email = data.get("email", "").strip()
        password = data.get("password", "")

        result = login_user(email=email, password=password)

        return jsonify({
            "ok": True,
            "data": result
        }), 200

    except AuthServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code