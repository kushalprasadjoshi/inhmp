import uuid
from sqlalchemy import Column, String, Enum, Boolean, Integer, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    hospital_id = Column(BINARY(16), ForeignKey('hospital.id'), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    phone = Column(String(20))
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(Enum('Patient','Doctor','HospitalAdmin','EmergencyOfficer','SystemAdmin'), nullable=False)
    is_active = Column(Boolean, default=True)
    version = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    hospital = relationship("Hospital")
    patient = relationship("Patient", back_populates="user", uselist=False)

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)