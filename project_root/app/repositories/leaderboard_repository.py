from sqlalchemy import func, case

from app.extensions import db
from app.models.models import LeaderboardScore, User, Run


def create_leaderboard_entry(user_id: int):
    entry = LeaderboardScore(
        user_id=user_id,
        score=0
    )
    db.session.add(entry)
    db.session.flush()
    return entry


def get_leaderboard_entry_by_user_id(user_id: int):
    return LeaderboardScore.query.filter_by(user_id=user_id).first()


def add_score_to_user(user_id: int, score_to_add: int):
    entry = get_leaderboard_entry_by_user_id(user_id)

    if not entry:
        entry = LeaderboardScore(
            user_id=user_id,
            score=0
        )
        db.session.add(entry)
        db.session.flush()

    entry.score += score_to_add
    db.session.add(entry)
    return entry


def get_full_leaderboard():
    success_case = case((Run.status == "extracted", 1), else_=0)

    rows = (
        db.session.query(
            User.id.label("user_id"),
            User.nickname.label("nickname"),
            LeaderboardScore.score.label("score"),
            func.count(Run.id).label("runs_count"),
            func.coalesce(func.sum(success_case), 0).label("wins_count")
        )
        .join(LeaderboardScore, LeaderboardScore.user_id == User.id)
        .outerjoin(Run, Run.user_id == User.id)
        .group_by(User.id, User.nickname, LeaderboardScore.score)
        .order_by(LeaderboardScore.score.desc(), User.nickname.asc())
        .all()
    )

    return rows


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()