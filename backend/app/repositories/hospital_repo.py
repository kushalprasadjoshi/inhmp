from uuid import UUID
from sqlalchemy.orm import Session
from app.models.hospital import Hospital
from app.repositories.base import BaseRepository

class HospitalRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Hospital)

    def get_by_name(self, name: str):
        return self.db.query(Hospital).filter(Hospital.name == name).first()

    def list_all(self):
        return self.db.query(Hospital).filter(Hospital.is_active == True).all()