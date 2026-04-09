from datetime import datetime

from app.extensions import db
from app.models.models import Inventory


def get_inventory_by_user_id(user_id: int):
    return (
        Inventory.query
        .filter_by(user_id=user_id)
        .order_by(Inventory.item_code.asc())
        .all()
    )


def get_inventory_item(user_id: int, item_code: str):
    return Inventory.query.filter_by(user_id=user_id, item_code=item_code).first()


def add_or_update_inventory_item(user_id: int, item_code: str, quantity: int):
    item = get_inventory_item(user_id, item_code)

    if item:
        item.quantity += quantity
        item.updated_at = datetime.utcnow()
        db.session.add(item)
        return item

    item = Inventory(
        user_id=user_id,
        item_code=item_code,
        quantity=quantity,
        updated_at=datetime.utcnow()
    )
    db.session.add(item)
    db.session.flush()
    return item


def set_inventory_item_quantity(user_id: int, item_code: str, quantity: int):
    item = get_inventory_item(user_id, item_code)

    if not item:
        item = Inventory(
            user_id=user_id,
            item_code=item_code,
            quantity=quantity,
            updated_at=datetime.utcnow()
        )
        db.session.add(item)
        db.session.flush()
        return item

    item.quantity = quantity
    item.updated_at = datetime.utcnow()
    db.session.add(item)
    return item


def remove_inventory_item(user_id: int, item_code: str):
    item = get_inventory_item(user_id, item_code)
    if not item:
        return False

    db.session.delete(item)
    return True


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()