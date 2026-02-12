import uuid
from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BINARY
from app.core.database import Base

class Hospital(Base):
    __tablename__ = "hospital"

    # ❌ WRONG: default=uuid.uuid4  → stores Python UUID object, not bytes
    # ✅ CORRECT: default=lambda: uuid.uuid4().bytes
    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    name = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    address = Column(String(500))
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)