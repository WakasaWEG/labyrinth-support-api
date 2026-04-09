from datetime import datetime

from app.extensions import db
from app.models.models import GameEvent


def create_event(user_id: int, run_id, event_type: str, payload: dict):
    event = GameEvent(
        user_id=user_id,
        run_id=run_id,
        event_type=event_type,
        payload_json=payload,
        created_at=datetime.utcnow()
    )
    db.session.add(event)
    db.session.flush()
    return event


def get_events_by_user_id(user_id: int):
    return (
        GameEvent.query
        .filter_by(user_id=user_id)
        .order_by(GameEvent.created_at.desc())
        .all()
    )


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()