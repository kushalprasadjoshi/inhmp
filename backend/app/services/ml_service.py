import joblib
import numpy as np
import pandas as pd
from pathlib import Path

# Get absolute path to model files
BASE_DIR = Path(__file__).parent.parent
DIABETES_MODEL_PATH = BASE_DIR / "ml_models" / "diabetes_model.pkl"
HEART_MODEL_PATH = BASE_DIR / "ml_models" / "heart_model.pkl"

# Load models once at startup
_diabetes_model = None
_heart_model = None

def load_models():
    global _diabetes_model, _heart_model
    if _diabetes_model is None:
        _diabetes_model = joblib.load(DIABETES_MODEL_PATH)
    if _heart_model is None:
        _heart_model = joblib.load(HEART_MODEL_PATH)

def predict_diabetes(features: dict):
    """
    Expects features: pregnancies, glucose, blood_pressure, skin_thickness,
                     insulin, bmi, diabetes_pedigree, age
    """
    load_models()
    # Convert to numpy array (order must match training)
    feature_names = [
        'pregnancies', 'glucose', 'blood_pressure', 'skin_thickness',
        'insulin', 'bmi', 'diabetes_pedigree', 'age'
    ]
    # Ensure correct order
    input_array = np.array([[features[name] for name in feature_names]])
    prediction = _diabetes_model.predict(input_array)[0]
    probability = _diabetes_model.predict_proba(input_array)[0][1]  # positive class
    return {
        "prediction": int(prediction),
        "probability": float(probability),
        "message": "Diabetic" if prediction == 1 else "Non-diabetic"
    }

def predict_heart(features: dict):
    """
    Expects features: age, sex, cp, trestbps, chol, fbs, restecg,
                     thalach, exang, oldpeak, slope, ca, thal
    """
    load_models()
    feature_names = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    input_array = np.array([[features[name] for name in feature_names]])
    prediction = _heart_model.predict(input_array)[0]
    probability = _heart_model.predict_proba(input_array)[0][1]
    return {
        "prediction": int(prediction),
        "probability": float(probability),
        "message": "Heart disease present" if prediction == 1 else "No heart disease"
    }