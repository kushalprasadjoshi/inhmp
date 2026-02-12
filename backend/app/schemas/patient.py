from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    national_id: Optional[str] = None
    date_of_birth: date
    blood_group: Optional[str] = None
    allergies: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: UUID
    user_id: UUID
    full_name: str
    email: str
    phone: Optional[str]

    class Config:
        from_attributes = True