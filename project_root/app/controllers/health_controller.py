from flask import jsonify
from sqlalchemy import text

from app.extensions import db


def health_check():
    return jsonify({
        "ok": True,
        "data": {
            "status": "healthy"
        }
    }), 200


def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({
            "ok": True,
            "data": {
                "db": "connected"
            }
        }), 200
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": {
                "code": "DB_CONNECTION_ERROR",
                "message": str(e)
            }
        }), 500