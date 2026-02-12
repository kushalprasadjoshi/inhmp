from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class ConsentRequest(BaseModel):
    patient_id: UUID
    accessing_hospital_id: UUID

class OTPVerify(BaseModel):
    consent_id: UUID
    otp: str

class ConsentOut(BaseModel):
    id: UUID
    patient_id: UUID
    accessing_hospital_id: UUID
    status: str
    valid_until: Optional[datetime]

    class Config:
        from_attributes = True