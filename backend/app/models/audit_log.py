import uuid
from sqlalchemy import Column, String, TIMESTAMP, JSON, ForeignKey, text
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    user_id = Column(BINARY(16), ForeignKey('user.id'), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(BINARY(16))
    old_value = Column(JSON)
    new_value = Column(JSON)
    ip_address = Column(String(45))
    user_agent = Column(String(500))
    timestamp = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User")

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)