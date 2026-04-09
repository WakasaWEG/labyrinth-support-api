import uuid

from flask import g, request


def register_request_id_middleware(app):
    @app.before_request
    def set_request_id():
        g.request_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-Id"] = g.get("request_id", "")
        return response