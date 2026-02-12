import uuid
from sqlalchemy import Column, String, Date, Boolean, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from app.core.database import Base

class Visit(Base):
    __tablename__ = "visit"

    id = Column(BINARY(16), primary_key=True, default=lambda: uuid.uuid4().bytes)
    patient_id = Column(BINARY(16), ForeignKey('patient.id'), nullable=False)
    hospital_id = Column(BINARY(16), ForeignKey('hospital.id'), nullable=False)
    doctor_id = Column(BINARY(16), ForeignKey('user.id'), nullable=False)
    visit_date = Column(Date, nullable=False)
    diagnosis_code = Column(String(20))   # ICD-10
    symptoms = Column(String(1000))
    treatment = Column(String(1000))
    medication = Column(String(500))
    lab_result = Column(String(1000))
    is_emergency = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    patient = relationship("Patient")
    hospital = relationship("Hospital")
    doctor = relationship("User")

    @property
    def uuid(self):
        return uuid.UUID(bytes=self.id)