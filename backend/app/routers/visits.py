from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.visit import VisitCreate, VisitOut
from app.services.visit_service import VisitService
from app.models.user import User

router = APIRouter(prefix="/visits", tags=["Visits"])

@router.post("/", response_model=VisitOut)
def create_visit(
    visit: VisitCreate,
    db: Session = Depends(get_db),
    doctor: User = Depends(require_role(["Doctor"]))
):
    service = VisitService(db)
    try:
        new_visit = service.create_visit(
            doctor_id=doctor.id,
            hospital_id=doctor.hospital_id,  # doctor belongs to a hospital
            visit_data=visit
        )
        return VisitOut(
            id=UUID(bytes=new_visit.id),
            patient_id=UUID(bytes=new_visit.patient_id),
            hospital_id=UUID(bytes=new_visit.hospital_id),
            doctor_id=UUID(bytes=new_visit.doctor_id),
            visit_date=new_visit.visit_date,
            diagnosis_code=new_visit.diagnosis_code,
            symptoms=new_visit.symptoms,
            treatment=new_visit.treatment,
            medication=new_visit.medication,
            lab_result=new_visit.lab_result,
            is_emergency=new_visit.is_emergency,
            created_at=new_visit.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/patient/{patient_id}")
def get_patient_visits(
    patient_id: UUID,
    db: Session = Depends(get_db),
    doctor: User = Depends(require_role(["Doctor"]))
):
    service = VisitService(db)
    visits = service.repo.get_by_patient(patient_id)
    return [
        {
            "id": UUID(bytes=v.id),
            "visit_date": v.visit_date,
            "diagnosis_code": v.diagnosis_code,
            "doctor_id": UUID(bytes=v.doctor_id)
        }
        for v in visits
    ]