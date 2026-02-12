from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import require_role
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import DiseaseCount, TrendPoint, OutbreakAlert

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/disease-summary", response_model=List[DiseaseCount])
def disease_summary(
    db: Session = Depends(get_db),
    _=Depends(require_role(["SystemAdmin", "EmergencyOfficer"]))
):
    service = AnalyticsService(db)
    return service.get_disease_summary()

@router.get("/trends", response_model=List[TrendPoint])
def trends(
    db: Session = Depends(get_db),
    _=Depends(require_role(["SystemAdmin", "EmergencyOfficer"]))
):
    service = AnalyticsService(db)
    return service.get_trends()

@router.get("/outbreak-alerts", response_model=List[OutbreakAlert])
def outbreak_alerts(
    db: Session = Depends(get_db),
    _=Depends(require_role(["SystemAdmin", "EmergencyOfficer"]))
):
    service = AnalyticsService(db)
    return service.get_outbreak_alerts()