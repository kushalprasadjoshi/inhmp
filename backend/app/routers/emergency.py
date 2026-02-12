from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.emergency import EmergencyAccessRequest, EmergencyAccessOut
from app.services.emergency_service import EmergencyService
from app.models.user import User

router = APIRouter(prefix="/emergency", tags=["Emergency"])

@router.post("/access", response_model=EmergencyAccessOut)
def emergency_access(
    request: EmergencyAccessRequest,
    db: Session = Depends(get_db),
    officer: User = Depends(require_role(["EmergencyOfficer", "Doctor"]))
):
    service = EmergencyService(db)
    try:
        log = service.grant_emergency_access(
            officer_id=officer.id,
            hospital_id=officer.hospital_id,
            request=request
        )
        return EmergencyAccessOut(
            id=UUID(bytes=log.id),
            patient_id=UUID(bytes=log.patient_id),
            hospital_id=UUID(bytes=log.hospital_id),
            officer_id=UUID(bytes=log.emergency_officer_id),
            reason=log.reason,
            justification=log.justification,
            accessed_at=log.accessed_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))