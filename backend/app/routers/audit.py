from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.audit import AuditLogOut
from app.services.audit_service import AuditService
from app.models.user import User

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/logs", response_model=List[AuditLogOut])
def get_audit_logs(
    db: Session = Depends(get_db),
    admin: User = Depends(require_role(["SystemAdmin"]))
):
    service = AuditService(db)
    logs = service.get_recent_logs(limit=200)
    return [
        AuditLogOut(
            id=UUID(bytes=log.id),
            user_id=UUID(bytes=log.user_id) if log.user_id else None,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=UUID(bytes=log.resource_id) if log.resource_id else None,
            old_value=log.old_value,
            new_value=log.new_value,
            ip_address=log.ip_address,
            user_agent=log.user_agent,
            timestamp=log.timestamp
        )
        for log in logs
    ]