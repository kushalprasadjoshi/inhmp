from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password: str
    full_name: str
    role: str
    hospital_id: Optional[UUID] = None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str