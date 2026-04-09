from app.repositories.leaderboard_repository import get_full_leaderboard


class LeaderboardServiceError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def get_leaderboard():
    try:
        rows = get_full_leaderboard()

        items = []
        rank = 1

        for row in rows:
            items.append({
                "rank": rank,
                "userId": row.user_id,
                "nickname": row.nickname,
                "score": int(row.score or 0),
                "runsCount": int(row.runs_count or 0),
                "winsCount": int(row.wins_count or 0)
            })
            rank += 1

        return {
            "items": items
        }
    except Exception:
        raise LeaderboardServiceError("LEADERBOARD_FETCH_FAILED", "Failed to fetch leaderboard", 500)