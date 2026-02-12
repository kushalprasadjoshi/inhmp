from sqlalchemy.orm import Session
from uuid import uuid4
from app.repositories.audit_repo import AuditRepository

class AuditService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = AuditRepository(db)

    def log_action(self, user_id, action, resource_type=None, resource_id=None,
                   old_value=None, new_value=None, ip_address=None, user_agent=None):
        log_entry = self.repo.create(
            id=uuid4().bytes,
            user_id=user_id.bytes if user_id else None,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id.bytes if resource_id else None,
            old_value=old_value,
            new_value=new_value,
            ip_address=ip_address,
            user_agent=user_agent
        )
        return log_entry

    def get_recent_logs(self, limit=100):
        return self.repo.list_recent(limit)