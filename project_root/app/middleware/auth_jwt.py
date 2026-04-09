from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def auth_required(roles=None):
    roles = roles or []

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt()

                if roles:
                    user_roles = claims.get("roles", [])
                    if not any(role in user_roles for role in roles):
                        return jsonify({
                            "ok": False,
                            "error": {
                                "code": "FORBIDDEN",
                                "message": "You do not have permission to access this resource"
                            }
                        }), 403

                return fn(*args, **kwargs)
            except Exception:
                return jsonify({
                    "ok": False,
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "Missing or invalid token"
                    }
                }), 401

        return wrapper
    return decorator