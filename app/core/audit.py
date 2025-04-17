from datetime import datetime
from app.core.logger import log_event


def audit_trail(user_id: int, action: str):
    timestamp = datetime.utcnow().isoformat()
    log_event(f"User {user_id} performed action: {action} at {timestamp}")
