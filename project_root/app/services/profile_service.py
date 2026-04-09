from app.repositories.user_repository import get_user_by_id
from app.repositories.progress_repository import get_progress_by_user_id


class ProfileServiceError(Exception):
    def __init__(self, code, message, status):
        self.code = code
        self.message = message
        self.status = status
        super().__init__(message)


def get_profile(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise ProfileServiceError("USER_NOT_FOUND", "User not found", 404)

    progress = get_progress_by_user_id(user_id)

    return {
        "userId": user.id,
        "email": user.email,
        "nickname": user.nickname,
        "isBanned": user.is_banned,
        "progress": {
            "level": progress.level if progress else 1,
            "xp": progress.xp if progress else 0,
            "softCurrency": progress.soft_currency if progress else 0,
            "hardCurrency": progress.hard_currency if progress else 0
        }
    }