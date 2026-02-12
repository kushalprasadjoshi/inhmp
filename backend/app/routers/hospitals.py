from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.hospital import HospitalCreate, HospitalOut
from app.services.hospital_service import HospitalService

router = APIRouter(prefix="/hospitals", tags=["Hospitals"])

@router.get("/", response_model=List[HospitalOut])
def list_hospitals(db: Session = Depends(get_db)):
    service = HospitalService(db)
    hospitals = service.get_all_hospitals()
    return [
        HospitalOut(
            id=UUID(bytes=h.id),
            name=h.name,
            district=h.district
        )
        for h in hospitals
    ]

@router.post("/", response_model=HospitalOut)
def create_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db),
    admin = Depends(require_role(["HospitalAdmin", "SystemAdmin"]))
):
    service = HospitalService(db)
    try:
        new_hospital = service.create_hospital(hospital)
        return HospitalOut(
            id=UUID(bytes=new_hospital.id),
            name=new_hospital.name,
            district=new_hospital.district
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))