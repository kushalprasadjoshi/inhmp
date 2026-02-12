from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.schemas.patient import PatientCreate, PatientOut
from app.services.patient_service import PatientService
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Only Patient role can register themselves; HospitalAdmin can register any
    if current_user.role not in ["Patient", "HospitalAdmin", "SystemAdmin"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    service = PatientService(db)
    try:
        new_patient = service.create_patient(current_user.id, patient)
        return PatientOut(
            id=UUID(bytes=new_patient.id),
            user_id=UUID(bytes=new_patient.user_id),
            full_name=current_user.full_name,
            email=current_user.email,
            phone=current_user.phone,
            national_id=new_patient.national_id,
            date_of_birth=new_patient.date_of_birth,
            blood_group=new_patient.blood_group,
            allergies=new_patient.allergies,
            emergency_contact=new_patient.emergency_contact
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=PatientOut)
def get_my_patient(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Patient"]))
):
    service = PatientService(db)
    try:
        patient = service.get_patient_profile(current_user.id)
        return PatientOut(
            id=UUID(bytes=patient.id),
            user_id=UUID(bytes=patient.user_id),
            full_name=current_user.full_name,
            email=current_user.email,
            phone=current_user.phone,
            national_id=patient.national_id,
            date_of_birth=patient.date_of_birth,
            blood_group=patient.blood_group,
            allergies=patient.allergies,
            emergency_contact=patient.emergency_contact
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/search")
def search_patients(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["Doctor", "HospitalAdmin"]))
):
    service = PatientService(db)
    patients = service.repo.search(q)
    result = []
    for p in patients:
        user = service.user_repo.get(UUID(bytes=p.user_id))
        result.append({
            "id": UUID(bytes=p.id),
            "full_name": user.full_name,
            "national_id": p.national_id,
            "date_of_birth": p.date_of_birth.isoformat()
        })
    return result