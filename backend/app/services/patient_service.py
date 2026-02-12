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
        # ===== ROBUST UUID/BYTES HANDLING =====
        from uuid import UUID
        
        # Convert user_id to bytes – works whether it's UUID, bytes, or string
        if isinstance(user_id, UUID):
            user_id_bytes = user_id.bytes
        elif isinstance(user_id, bytes):
            user_id_bytes = user_id          # ✅ already bytes – NO .bytes CALL!
        else:
            user_id_bytes = UUID(str(user_id)).bytes
    
        # Get user – need to convert bytes to UUID for repo.get
        user = self.user_repo.get(UUID(bytes=user_id_bytes))
        if not user:
            raise ValueError("User not found")
    
        # Check existing patient (repo.get_by_user_id already handles bytes)
        existing = self.repo.get_by_user_id(user_id_bytes)
        if existing:
            raise ValueError("Patient profile already exists")
    
        # Create patient – pass bytes directly
        return self.repo.create(
            id=uuid4().bytes,
            user_id=user_id_bytes,           # ✅ bytes – correct
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