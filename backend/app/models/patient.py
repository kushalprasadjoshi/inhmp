import uuid
from sqlalchemy import Column, String, Date, Boolean, Integer, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Patient(Base):
    __tablename__ = "patient"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    user_id = Column(BINARY(16), ForeignKey('user.id'), unique=True, nullable=False)
    national_id = Column(String(50))
    date_of_birth = Column(Date, nullable=False)
    blood_group = Column(String(5))
    allergies = Column(String(500))
    emergency_contact = Column(String(20))
    is_anonymized = Column(Boolean, default=False)
    version = Column(Integer, default=1)

    # ✅ CRITICAL: This relationship must match the one in User model
    user = relationship("User", back_populates="patient")

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)