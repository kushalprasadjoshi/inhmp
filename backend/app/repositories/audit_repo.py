from uuid import UUID
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from app.repositories.base import BaseRepository

class AuditRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, AuditLog)

    def list_recent(self, limit: int = 100):
        return self.db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()

    def filter_by_user(self, user_id: UUID):
        return self.db.query(AuditLog).filter(AuditLog.user_id == user_id.bytes).all()