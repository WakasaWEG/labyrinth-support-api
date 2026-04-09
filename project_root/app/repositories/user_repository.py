from datetime import datetime

from app.extensions import db
from app.models.models import User, Role, UserRole, PlayerProgress


def get_user_by_email(email: str):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id: int):
    return User.query.filter_by(id=user_id).first()


def create_user(email: str, password_hash: str, nickname: str):
    user = User(
        email=email,
        password_hash=password_hash,
        nickname=nickname,
        created_at=datetime.utcnow(),
        last_login_at=None,
        is_banned=False
    )
    db.session.add(user)
    db.session.flush()
    return user


def get_role_by_name(name: str):
    return Role.query.filter_by(name=name).first()


def assign_role(user_id: int, role_id: int):
    user_role = UserRole(
        user_id=user_id,
        role_id=role_id,
        assigned_at=datetime.utcnow()
    )
    db.session.add(user_role)
    return user_role


def create_player_progress(user_id: int):
    progress = PlayerProgress(
        user_id=user_id,
        level=1,
        xp=0,
        soft_currency=100,
        hard_currency=0,
        updated_at=datetime.utcnow()
    )
    db.session.add(progress)
    return progress


def update_last_login(user: User):
    user.last_login_at = datetime.utcnow()
    db.session.add(user)


def get_user_role_names(user_id: int):
    rows = (
        db.session.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return [row[0] for row in rows]


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()