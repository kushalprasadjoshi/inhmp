from pydantic import BaseModel
from typing import List, Dict, Any

class DiseaseCount(BaseModel):
    district: str
    diagnosis_code: str
    cases: int

class TrendPoint(BaseModel):
    week: int
    cases: int

class OutbreakAlert(BaseModel):
    district: str
    date: str
    daily_cases: int
    avg_4day: float