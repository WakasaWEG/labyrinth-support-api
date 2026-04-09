def validate_register_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    email = data.get("email")
    password = data.get("password")
    nickname = data.get("nickname")

    if not email or not isinstance(email, str):
        return False, "email is required"
    if not password or not isinstance(password, str):
        return False, "password is required"
    if not nickname or not isinstance(nickname, str):
        return False, "nickname is required"

    return True, None


def validate_login_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    email = data.get("email")
    password = data.get("password")

    if not email or not isinstance(email, str):
        return False, "email is required"
    if not password or not isinstance(password, str):
        return False, "password is required"

    return True, None


def validate_run_finish_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    if "runId" not in data:
        return False, "runId is required"
    if "isSuccess" not in data:
        return False, "isSuccess is required"

    return True, None


def validate_event_payload(data):
    if not isinstance(data, dict):
        return False, "Request body must be a JSON object"

    event_type = data.get("eventType")
    payload = data.get("payload")

    if not event_type or not isinstance(event_type, str):
        return False, "eventType is required"
    if payload is None or not isinstance(payload, dict):
        return False, "payload must be an object"

    return True, None