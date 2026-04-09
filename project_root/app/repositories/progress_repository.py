from app.models.models import PlayerProgress


def get_progress_by_user_id(user_id: int):
    return PlayerProgress.query.filter_by(user_id=user_id).first()