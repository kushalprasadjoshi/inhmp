from uuid import UUID
from sqlalchemy.orm import Session
from app.models.emergency_log import EmergencyAccessLog
from app.repositories.base import BaseRepository

class EmergencyRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, EmergencyAccessLog)

    def get_by_patient(self, patient_id: UUID):
        return self.db.query(EmergencyAccessLog).filter(
            EmergencyAccessLog.patient_id == patient_id.bytes
        ).all()