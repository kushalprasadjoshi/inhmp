import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
MODELS_DIR = os.path.join(BASE_DIR, 'backend/app/ml_models')

os.makedirs(MODELS_DIR, exist_ok=True)

DATASETS = {
    'diabetes': {
        'file_path': os.path.join(DATASET_DIR, 'diabetes.csv'),
        'target': 'diabetes',                     # <-- correct target column
        'numerical_features': [
            'age', 'bmi', 'hba1c_level', 'blood_glucose_level',
            'hypertension', 'heart_disease'       # binary, but ok as numeric
        ],
        'categorical_features': ['gender', 'smoking_history'],
        'zero_to_median': [],                    # <-- no zero replacement needed
        'scaler': 'standard',
        'models': {
            'RandomForest': {
                'n_estimators': [50, 100],
                'max_depth': [5, 10, None],
                'min_samples_split': [2, 5]
            },
            'LogisticRegression': {
                'C': [0.1, 1, 10],
                'solver': ['liblinear', 'lbfgs']
            }
        }
    },
    'heart': {
        'file_path': os.path.join(DATASET_DIR, 'heart.csv'),
        'target': 'target',                     # already lowercase
        'numerical_features': ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca'],
        'categorical_features': ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal'],
        'missing_values': {'ca': 0, 'thal': 1},
        'scaler': 'standard',
        'models': {
            'RandomForest': {
                'n_estimators': [50, 100],
                'max_depth': [5, 10, None],
                'min_samples_split': [2, 5]
            },
            'LogisticRegression': {
                'C': [0.1, 1, 10],
                'solver': ['liblinear', 'lbfgs']
            }
        }
    }
}