from datetime import datetime

from app.extensions import db
from app.models.models import Run, RunResult, PlayerProgress


def get_active_run_by_user_id(user_id: int):
    return Run.query.filter_by(user_id=user_id, status="started").first()


def create_run(user_id: int):
    run = Run(
        user_id=user_id,
        status="started",
        started_at=datetime.utcnow(),
        ended_at=None
    )
    db.session.add(run)
    db.session.flush()
    return run


def get_run_by_id(run_id: int):
    return Run.query.filter_by(id=run_id).first()


def update_run_status(run: Run, status: str):
    run.status = status
    run.ended_at = datetime.utcnow()
    db.session.add(run)
    return run


def create_run_result(run_id: int, is_success: bool, rooms_visited: int, loot_value: int, duration_seconds: int, ended_reason: str):
    run_result = RunResult(
        run_id=run_id,
        is_success=is_success,
        rooms_visited=rooms_visited,
        loot_value=loot_value,
        duration_seconds=duration_seconds,
        ended_reason=ended_reason
    )
    db.session.add(run_result)
    return run_result


def get_progress_by_user_id(user_id: int):
    return PlayerProgress.query.filter_by(user_id=user_id).first()


def update_progress_after_run(user_id: int, xp_gained: int, soft_currency_gained: int):
    progress = PlayerProgress.query.filter_by(user_id=user_id).first()
    if not progress:
        return None

    progress.xp += xp_gained
    progress.soft_currency += soft_currency_gained
    progress.updated_at = datetime.utcnow()

    db.session.add(progress)
    return progress


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()