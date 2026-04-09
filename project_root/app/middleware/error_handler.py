from flask import jsonify, g


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "ok": False,
            "error": {
                "code": "NOT_FOUND",
                "message": "Endpoint not found",
                "requestId": g.get("request_id")
            }
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "ok": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "Internal server error",
                "requestId": g.get("request_id")
            }
        }), 500