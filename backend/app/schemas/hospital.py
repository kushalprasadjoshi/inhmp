from pydantic import BaseModel
from uuid import UUID

class HospitalCreate(BaseModel):
    name: str
    district: str
    address: str = None
    phone: str = None
    email: str = None

class HospitalOut(BaseModel):
    id: UUID
    name: str
    district: str