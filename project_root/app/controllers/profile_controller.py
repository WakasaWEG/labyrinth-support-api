from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.profile_service import get_profile, ProfileServiceError


@jwt_required()
def profile():
    try:
        user_id = int(get_jwt_identity())

        result = get_profile(user_id)

        return jsonify({
            "ok": True,
            "data": result
        }), 200

    except ProfileServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status