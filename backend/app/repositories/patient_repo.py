from uuid import UUID
from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.repositories.base import BaseRepository

class PatientRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Patient)

    def get_by_user_id(self, user_id):
        """
        Get patient profile by user_id.
        user_id can be UUID object or bytes.
        """
        # Convert UUID to bytes if needed
        if isinstance(user_id, UUID):
            user_id_bytes = user_id.bytes
        else:
            # Assume it's already bytes
            user_id_bytes = user_id
        return self.db.query(Patient).filter(Patient.user_id == user_id_bytes).first()

    def search(self, query: str):
        from app.models.user import User
        return self.db.query(Patient).join(User).filter(
            (Patient.national_id.contains(query)) |
            (User.full_name.contains(query))
        ).all()