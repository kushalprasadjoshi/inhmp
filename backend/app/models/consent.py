import uuid
from sqlalchemy import Column, String, Enum, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Consent(Base):
    __tablename__ = "consent"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    patient_id = Column(BINARY(16), ForeignKey('patient.id'), nullable=False)
    granting_hospital_id = Column(BINARY(16), ForeignKey('hospital.id'), nullable=False)
    accessing_hospital_id = Column(BINARY(16), ForeignKey('hospital.id'), nullable=False)
    granted_by_user_id = Column(BINARY(16), ForeignKey('user.id'), nullable=False)
    otp_hash = Column(String(255))
    otp_expiry = Column(TIMESTAMP, nullable=True)
    status = Column(Enum('pending', 'active', 'expired', 'revoked'), default='pending')
    valid_from = Column(TIMESTAMP, nullable=True)
    valid_until = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    patient = relationship("Patient", foreign_keys=[patient_id])
    granting_hospital = relationship("Hospital", foreign_keys=[granting_hospital_id])
    accessing_hospital = relationship("Hospital", foreign_keys=[accessing_hospital_id])
    granted_by = relationship("User", foreign_keys=[granted_by_user_id])

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)