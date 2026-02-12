from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.consent import ConsentRequest, OTPVerify, ConsentOut
from app.services.consent_service import ConsentService
from app.models.user import User

router = APIRouter(prefix="/consent", tags=["Consent"])

@router.post("/request-otp")
def request_otp(
    request: ConsentRequest,
    db: Session = Depends(get_db),
    doctor: User = Depends(require_role(["Doctor"]))
):
    service = ConsentService(db)
    try:
        consent, otp = service.request_otp(
            doctor_id=doctor.id,
            granting_hospital_id=doctor.hospital_id,
            patient_id=request.patient_id,
            accessing_hospital_id=request.accessing_hospital_id
        )
        # In real life: send OTP via SMS; for hackathon return it (mock)
        return {
            "consent_id": UUID(bytes=consent.id),
            "otp": otp,   # REMOVE in production!
            "message": "OTP generated (mock: check response)"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/verify-otp")
def verify_otp_endpoint(
    payload: OTPVerify,
    db: Session = Depends(get_db),
    doctor: User = Depends(require_role(["Doctor"]))
):
    service = ConsentService(db)
    try:
        consent = service.verify_otp_and_activate(payload.consent_id, payload.otp)
        return {"message": "Consent activated", "consent_id": UUID(bytes=consent.id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check/{patient_id}")
def check_access(
    patient_id: UUID,
    db: Session = Depends(get_db),
    doctor: User = Depends(require_role(["Doctor"]))
):
    service = ConsentService(db)
    has_access = service.check_access(patient_id, doctor.hospital_id)
    return {"access_granted": has_access}