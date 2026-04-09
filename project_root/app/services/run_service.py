from app.repositories.run_repository import (
    get_active_run_by_user_id,
    create_run,
    get_run_by_id,
    update_run_status,
    create_run_result,
    update_progress_after_run,
    commit,
    rollback,
)
from app.repositories.leaderboard_repository import add_score_to_user


class RunServiceError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def start_run(user_id: int):
    active_run = get_active_run_by_user_id(user_id)
    if active_run:
        raise RunServiceError("ACTIVE_RUN_ALREADY_EXISTS", "User already has an active run", 409)

    try:
        run = create_run(user_id)
        commit()

        return {
            "runId": run.id,
            "status": run.status,
            "startedAt": run.started_at.isoformat() if run.started_at else None
        }
    except Exception:
        rollback()
        raise RunServiceError("RUN_START_FAILED", "Failed to start run", 500)


def finish_run(user_id: int, run_id: int, is_success: bool, rooms_visited: int, loot_value: int, duration_seconds: int):
    run = get_run_by_id(run_id)
    if not run:
        raise RunServiceError("RUN_NOT_FOUND", "Run not found", 404)

    if run.user_id != user_id:
        raise RunServiceError("FORBIDDEN", "Run does not belong to current user", 403)

    if run.status != "started":
        raise RunServiceError("RUN_ALREADY_FINISHED", "Run already finished", 409)

    ended_reason = "exit" if is_success else "death"
    new_status = "extracted" if is_success else "dead"

    xp_gained = 100 if is_success else 30
    soft_currency_gained = loot_value if is_success else 0
    leaderboard_score_gained = loot_value if is_success else 0

    try:
        update_run_status(run, new_status)
        create_run_result(
            run_id=run.id,
            is_success=is_success,
            rooms_visited=rooms_visited,
            loot_value=loot_value,
            duration_seconds=duration_seconds,
            ended_reason=ended_reason
        )

        update_progress_after_run(
            user_id=user_id,
            xp_gained=xp_gained,
            soft_currency_gained=soft_currency_gained
        )

        if leaderboard_score_gained > 0:
            add_score_to_user(user_id, leaderboard_score_gained)

        commit()

        return {
            "runId": run.id,
            "status": new_status,
            "isSuccess": is_success,
            "xpGained": xp_gained,
            "softCurrencyGained": soft_currency_gained,
            "leaderboardScoreGained": leaderboard_score_gained,
            "endedReason": ended_reason
        }
    except Exception:
        rollback()
        raise RunServiceError("RUN_FINISH_FAILED", "Failed to finish run", 500)