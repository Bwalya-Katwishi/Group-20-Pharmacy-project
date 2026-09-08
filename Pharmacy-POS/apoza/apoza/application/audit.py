from datetime import datetime

from sqlalchemy.orm import Session

from apoza.persistence.tables import AuditLog


class AuditLogger:
    """Pure Fabrication — keeps Sale and User free of logging details."""

    def __init__(self, db: Session):
        self.db = db

    def write(self, action: str, user_id: int | None = None, entity_name: str | None = None,
              entity_id: int | None = None, details: str | None = None) -> None:
        self.db.add(AuditLog(
            user_id=user_id,
            action=action,
            entity_name=entity_name,
            entity_id=entity_id,
            details=(details or "")[:500],
            occurred_at=datetime.utcnow(),
        ))
        self.db.flush()
