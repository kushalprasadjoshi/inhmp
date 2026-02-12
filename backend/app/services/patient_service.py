from sqlalchemy.orm import Session
from uuid import uuid4
from app.repositories.patient_repo import PatientRepository
from app.repositories.user_repo import UserRepository
from app.schemas.patient import PatientCreate

class PatientService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PatientRepository(db)
        self.user_repo = UserRepository(db)

    def create_patient(self, user_id, patient_data: PatientCreate):
        # Ensure user exists
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        # Check if patient already exists for this user
        existing = self.repo.get_by_user_id(user_id)
        if existing:
            raise ValueError("Patient profile already exists")
        return self.repo.create(
            id=uuid4().bytes,
            user_id=user_id.bytes,
            national_id=patient_data.national_id,
            date_of_birth=patient_data.date_of_birth,
            blood_group=patient_data.blood_group,
            allergies=patient_data.allergies,
            emergency_contact=patient_data.emergency_contact
        )

    def get_patient_profile(self, user_id):
        patient = self.repo.get_by_user_id(user_id)
        if not patient:
            raise ValueError("Patient profile not found")
        return patient