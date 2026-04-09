import bcrypt
from flask_jwt_extended import create_access_token

from app.repositories.user_repository import (
    get_user_by_email,
    create_user,
    get_role_by_name,
    assign_role,
    create_player_progress,
    update_last_login,
    get_user_role_names,
    commit,
    rollback,
)
from app.repositories.leaderboard_repository import create_leaderboard_entry


class AuthServiceError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_user(email: str, password: str, nickname: str):
    existing_user = get_user_by_email(email)
    if existing_user:
        raise AuthServiceError("EMAIL_ALREADY_EXISTS", "Email already exists", 409)

    if len(password) < 6:
        raise AuthServiceError("VALIDATION_ERROR", "Password must be at least 6 characters long", 400)

    if len(nickname.strip()) < 2:
        raise AuthServiceError("VALIDATION_ERROR", "Nickname must be at least 2 characters long", 400)

    try:
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user = create_user(
            email=email.strip(),
            password_hash=password_hash,
            nickname=nickname.strip()
        )

        player_role = get_role_by_name("player")
        if not player_role:
            raise AuthServiceError("ROLE_NOT_FOUND", "Role 'player' not found in database", 500)

        assign_role(user.id, player_role.id)
        create_player_progress(user.id)
        create_leaderboard_entry(user.id)

        commit()

        return {
            "userId": user.id
        }
    except AuthServiceError:
        rollback()
        raise
    except Exception:
        rollback()
        raise AuthServiceError("REGISTER_FAILED", "Failed to register user", 500)


def login_user(email: str, password: str):
    user = get_user_by_email(email.strip())
    if not user:
        raise AuthServiceError("INVALID_CREDENTIALS", "Invalid email or password", 401)

    if user.is_banned:
        raise AuthServiceError("USER_BANNED", "User is banned", 403)

    password_ok = bcrypt.checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8")
    )
    if not password_ok:
        raise AuthServiceError("INVALID_CREDENTIALS", "Invalid email or password", 401)

    try:
        update_last_login(user)
        commit()

        roles = get_user_role_names(user.id)

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"roles": roles}
        )

        return {
            "accessToken": access_token,
            "tokenType": "Bearer",
            "expiresInSeconds": 3600
        }
    except AuthServiceError:
        rollback()
        raise
    except Exception:
        rollback()
        raise AuthServiceError("LOGIN_FAILED", "Failed to login user", 500)