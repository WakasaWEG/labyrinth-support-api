from datetime import datetime
from app.extensions import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime, nullable=True)
    is_banned = db.Column(db.Boolean, nullable=False, default=False)


class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="RESTRICT"), primary_key=True)
    assigned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class PlayerProgress(db.Model):
    __tablename__ = "player_progress"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=1)
    xp = db.Column(db.Integer, nullable=False, default=0)
    soft_currency = db.Column(db.Integer, nullable=False, default=0)
    hard_currency = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    item_code = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Run(db.Model):
    __tablename__ = "runs"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.Enum("started", "extracted", "dead"), nullable=False, default="started")
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)


class RunResult(db.Model):
    __tablename__ = "run_results"

    run_id = db.Column(db.BigInteger, db.ForeignKey("runs.id", ondelete="CASCADE"), primary_key=True)
    is_success = db.Column(db.Boolean, nullable=False)
    rooms_visited = db.Column(db.Integer, nullable=False, default=0)
    loot_value = db.Column(db.Integer, nullable=False, default=0)
    duration_seconds = db.Column(db.Integer, nullable=False, default=0)
    ended_reason = db.Column(db.Enum("exit", "death"), nullable=False)


class LeaderboardScore(db.Model):
    __tablename__ = "leaderboard_scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    score = db.Column(db.Integer, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class GameEvent(db.Model):
    __tablename__ = "game_events"

    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    run_id = db.Column(db.BigInteger, db.ForeignKey("runs.id", ondelete="SET NULL"), nullable=True)
    event_type = db.Column(db.String(64), nullable=False)
    payload_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)