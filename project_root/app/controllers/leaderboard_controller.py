from flask import jsonify

from app.services.leaderboard_service import get_leaderboard, LeaderboardServiceError


def leaderboard():
    try:
        result = get_leaderboard()

        return jsonify({
            "ok": True,
            "data": result
        }), 200

    except LeaderboardServiceError as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": e.code,
                "message": e.message
            }
        }), e.status_code