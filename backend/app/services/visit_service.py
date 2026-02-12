from sqlalchemy.orm import Session
from uuid import uuid4
from app.repositories.visit_repo import VisitRepository
from app.repositories.patient_repo import PatientRepository
from app.schemas.visit import VisitCreate

class VisitService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = VisitRepository(db)
        self.patient_repo = PatientRepository(db)

    def create_visit(self, doctor_id, hospital_id, visit_data: VisitCreate):
        # Verify patient exists
        patient = self.patient_repo.get(visit_data.patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return self.repo.create(
            id=uuid4().bytes,
            patient_id=visit_data.patient_id.bytes,
            hospital_id=hospital_id.bytes,
            doctor_id=doctor_id.bytes,
            visit_date=visit_data.visit_date,
            diagnosis_code=visit_data.diagnosis_code,
            symptoms=visit_data.symptoms,
            treatment=visit_data.treatment,
            medication=visit_data.medication,
            lab_result=visit_data.lab_result,
            is_emergency=visit_data.is_emergency
        )