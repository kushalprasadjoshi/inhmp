import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from app.core.database import Base

class EmergencyAccessLog(Base):
    __tablename__ = "emergency_access_log"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    patient_id = Column(BINARY(16), ForeignKey('patient.id'), nullable=False)
    hospital_id = Column(BINARY(16), ForeignKey('hospital.id'), nullable=False)
    emergency_officer_id = Column(BINARY(16), ForeignKey('user.id'), nullable=False)
    reason = Column(String(500), nullable=False)
    justification = Column(String(1000), nullable=False)
    accessed_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    temporary_consent_id = Column(BINARY(16), ForeignKey('consent.id'), nullable=True)

    patient = relationship("Patient")
    hospital = relationship("Hospital")
    officer = relationship("User", foreign_keys=[emergency_officer_id])
    consent = relationship("Consent")

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)