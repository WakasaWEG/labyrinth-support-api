from app.repositories.event_repository import create_event, get_events_by_user_id, commit, rollback


class EventsServiceError(Exception):
    def __init__(self, code: str, message: str, status_code: int):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def post_event(user_id: int, run_id, event_type: str, payload: dict):
    try:
        event = create_event(
            user_id=user_id,
            run_id=run_id,
            event_type=event_type,
            payload=payload
        )
        commit()

        return {
            "eventId": event.id,
            "accepted": True
        }
    except Exception:
        rollback()
        raise EventsServiceError("EVENT_CREATE_FAILED", "Failed to create event", 500)


def get_user_events(user_id: int):
    try:
        events = get_events_by_user_id(user_id)

        return {
            "items": [
                {
                    "id": event.id,
                    "runId": event.run_id,
                    "eventType": event.event_type,
                    "payload": event.payload_json,
                    "createdAt": event.created_at.isoformat() if event.created_at else None
                }
                for event in events
            ]
        }
    except Exception:
        raise EventsServiceError("EVENTS_FETCH_FAILED", "Failed to fetch events", 500)