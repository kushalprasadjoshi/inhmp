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
    Expects PIMA-style features from frontend.
    Adapts to model that requires: age, bmi, glucose, etc. + extra columns.
    """
    load_models()
    
    # Define the exact columns your model expects (from the error message)
    required_columns = [
        'age', 'hypertension', 'heart_disease', 'bmi', 
        'hba1c_level', 'blood_glucose_level', 'gender', 'smoking_history'
    ]
    
    # Map incoming features to model columns with sensible defaults
    row = {
        'age': features.get('age', 30),
        'bmi': features.get('bmi', 25),
        'blood_glucose_level': features.get('glucose', 100),  # map glucose
        'hypertension': 1 if features.get('blood_pressure', 120) > 140 else 0,
        'heart_disease': 0,  # default, not provided
        'hba1c_level': 5.5,  # default
        'gender': 0,         # default (0 = female)
        'smoking_history': 0 # default (0 = never)
    }
    
    # Create DataFrame with correct column order
    input_df = pd.DataFrame([row])[required_columns]
    
    prediction = _diabetes_model.predict(input_df)[0]
    probability = _diabetes_model.predict_proba(input_df)[0][1]
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
    
    # Create DataFrame with proper column order
    input_df = pd.DataFrame([features], columns=feature_names)[feature_names]
    
    prediction = _heart_model.predict(input_df)[0]
    probability = _heart_model.predict_proba(input_df)[0][1]
    return {
        "prediction": int(prediction),
        "probability": float(probability),
        "message": "Heart disease present" if prediction == 1 else "No heart disease"
    }