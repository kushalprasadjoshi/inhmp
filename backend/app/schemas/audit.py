from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Any

class AuditLogOut(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    resource_type: Optional[str]
    resource_id: Optional[UUID]
    old_value: Optional[dict]
    new_value: Optional[dict]
    ip_address: Optional[str]
    user_agent: Optional[str]
    timestamp: datetime

    class Config:
        from_attributes = True