from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from app.repositories.emergency_repo import EmergencyRepository
from app.repositories.consent_repo import ConsentRepository
from app.repositories.patient_repo import PatientRepository
from app.schemas.emergency import EmergencyAccessRequest

class EmergencyService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = EmergencyRepository(db)
        self.consent_repo = ConsentRepository(db)
        self.patient_repo = PatientRepository(db)

    def grant_emergency_access(self, officer_id, hospital_id, request: EmergencyAccessRequest):
        patient = self.patient_repo.get(request.patient_id)
        if not patient:
            raise ValueError("Patient not found")

        # Create emergency log
        log_entry = self.repo.create(
            id=uuid4().bytes,
            patient_id=request.patient_id.bytes,
            hospital_id=hospital_id.bytes,
            emergency_officer_id=officer_id.bytes,
            reason=request.reason,
            justification=request.justification
        )

        # Optionally create a temporary consent (5 minutes)
        from app.models.consent import Consent
        temp_consent_id = uuid4().bytes
        temp_consent = Consent(
            id=temp_consent_id,
            patient_id=request.patient_id.bytes,
            granting_hospital_id=hospital_id.bytes,
            accessing_hospital_id=hospital_id.bytes,
            granted_by_user_id=officer_id.bytes,
            status='active',
            valid_from=datetime.utcnow(),
            valid_until=datetime.utcnow() + timedelta(minutes=5)
        )
        self.db.add(temp_consent)
        log_entry.temporary_consent_id = temp_consent_id
        self.db.commit()
        return log_entry