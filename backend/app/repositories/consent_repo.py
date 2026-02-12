from uuid import UUID
from sqlalchemy.orm import Session
from app.models.consent import Consent
from app.repositories.base import BaseRepository

class ConsentRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Consent)

    def get_pending_by_patient_and_hospital(self, patient_id: UUID, hospital_id: UUID):
        return self.db.query(Consent).filter(
            Consent.patient_id == patient_id.bytes,
            Consent.accessing_hospital_id == hospital_id.bytes,
            Consent.status == 'pending'
        ).first()

    def get_active_consent(self, patient_id: UUID, hospital_id: UUID):
        from sqlalchemy import and_
        from datetime import datetime
        now = datetime.utcnow()
        return self.db.query(Consent).filter(
            and_(
                Consent.patient_id == patient_id.bytes,
                Consent.accessing_hospital_id == hospital_id.bytes,
                Consent.status == 'active',
                Consent.valid_from <= now,
                Consent.valid_until >= now
            )
        ).first()