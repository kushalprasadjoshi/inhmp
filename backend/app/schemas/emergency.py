from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class EmergencyAccessRequest(BaseModel):
    patient_id: UUID
    reason: str
    justification: str

class EmergencyAccessOut(BaseModel):
    id: UUID
    patient_id: UUID
    hospital_id: UUID
    officer_id: UUID
    reason: str
    justification: str
    accessed_at: datetime

    class Config:
        from_attributes = True