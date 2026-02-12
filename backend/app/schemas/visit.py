from pydantic import BaseModel
from uuid import UUID
from datetime import date, datetime
from typing import Optional

class VisitBase(BaseModel):
    patient_id: UUID
    visit_date: date
    diagnosis_code: Optional[str] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None
    medication: Optional[str] = None
    lab_result: Optional[str] = None
    is_emergency: bool = False

class VisitCreate(VisitBase):
    pass

class VisitOut(VisitBase):
    id: UUID
    hospital_id: UUID
    doctor_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True