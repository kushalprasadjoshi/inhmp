from uuid import UUID
from sqlalchemy.orm import Session
from app.models.visit import Visit
from app.repositories.base import BaseRepository

class VisitRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Visit)

    def get_by_patient(self, patient_id: UUID):
        return self.db.query(Visit).filter(Visit.patient_id == patient_id.bytes).all()