from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services import ml_service

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# ----- Diabetes input schema -----
class DiabetesFeatures(BaseModel):
    pregnancies: float = Field(..., ge=0, le=20)
    glucose: float = Field(..., ge=0, le=300)
    blood_pressure: float = Field(..., ge=0, le=200)
    skin_thickness: float = Field(..., ge=0, le=100)
    insulin: float = Field(..., ge=0, le=1000)
    bmi: float = Field(..., ge=0, le=70)
    diabetes_pedigree: float = Field(..., ge=0, le=3)
    age: float = Field(..., ge=0, le=120)

class DiabetesPredictionOut(BaseModel):
    prediction: int
    probability: float
    message: str

# ----- Heart disease input schema -----
class HeartFeatures(BaseModel):
    age: float = Field(..., ge=0, le=120)
    sex: int = Field(..., ge=0, le=1)
    cp: int = Field(..., ge=0, le=3)
    trestbps: float = Field(..., ge=0, le=300)
    chol: float = Field(..., ge=0, le=600)
    fbs: int = Field(..., ge=0, le=1)
    restecg: int = Field(..., ge=0, le=2)
    thalach: float = Field(..., ge=0, le=250)
    exang: int = Field(..., ge=0, le=1)
    oldpeak: float = Field(..., ge=0, le=10)
    slope: int = Field(..., ge=0, le=2)
    ca: int = Field(..., ge=0, le=4)
    thal: int = Field(..., ge=1, le=3)

class HeartPredictionOut(BaseModel):
    prediction: int
    probability: float
    message: str

# ----- Endpoints (public – no auth required) -----
@router.post("/predict/diabetes", response_model=DiabetesPredictionOut)
async def predict_diabetes(features: DiabetesFeatures):
    try:
        return ml_service.predict_diabetes(features.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/predict/heart", response_model=HeartPredictionOut)
async def predict_heart(features: HeartFeatures):
    try:
        return ml_service.predict_heart(features.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# ----- Health check for models -----
@router.get("/health")
async def model_health():
    try:
        ml_service.load_models()
        return {"status": "models loaded", "diabetes": True, "heart": True}
    except Exception as e:
        return {"status": "error", "detail": str(e)}