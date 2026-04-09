from flask import Flask

from app.config import Config
from app.extensions import db, jwt, cors
from app.middleware.error_handler import register_error_handlers
from app.middleware.request_id import register_request_id_middleware


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    register_request_id_middleware(app)
    register_error_handlers(app)
    register_blueprints(app)

    return app


def register_blueprints(app):
    from app.routes.health_routes import health_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.profile_routes import profile_bp
    from app.routes.run_routes import run_bp
    from app.routes.events_routes import events_bp
    from app.routes.leaderboard_routes import leaderboard_bp

    app.register_blueprint(health_bp, url_prefix="/api/v1/health")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(profile_bp, url_prefix="/api/v1/profile")
    app.register_blueprint(run_bp, url_prefix="/api/v1/run")
    app.register_blueprint(events_bp, url_prefix="/api/v1/events")
    app.register_blueprint(leaderboard_bp, url_prefix="/api/v1/leaderboard")