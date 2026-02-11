from sqlalchemy import Column, String, Boolean, TIMESTAMP, text
from sqlalchemy.dialects.mysql import BINARY
import uuid

from backend.app.core.database import Base

class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(BINARY(16), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    address = Column(String)
    phone = Column(String(20))
    email = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))