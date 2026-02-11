import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from config import DATASETS, MODELS_DIR
from preprocess import load_and_clean, get_preprocessor
from utils import save_model, evaluate

def train_dataset(dataset_name):
    """Train and save best model for a given dataset."""
    print(f"\n===== Training {dataset_name.upper()} =====")
    config = DATASETS[dataset_name]
    
    # 1. Load and clean data
    df = load_and_clean(dataset_name, config)
    X = df.drop(columns=[config['target']])
    y = df[config['target']]
    
    # 2. Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Create preprocessor
    preprocessor = get_preprocessor(dataset_name, config)
    
    best_score = 0
    best_estimator = None
    best_model_name = None
    
    # 4. Iterate over models defined in config
    for model_name, params in config['models'].items():
        print(f"\nTuning {model_name}...")
        
        if model_name == 'RandomForest':
            clf = RandomForestClassifier(random_state=42)
        elif model_name == 'LogisticRegression':
            clf = LogisticRegression(random_state=42, max_iter=1000)
        else:
            continue
        
        # Create pipeline
        pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        # Parameter grid: prefix with 'classifier__'
        param_grid = {f'classifier__{k}': v for k, v in params.items()}
        
        # Grid search
        grid = GridSearchCV(pipeline, param_grid, cv=5, scoring='roc_auc', n_jobs=-1)
        grid.fit(X_train, y_train)
        
        print(f"Best params: {grid.best_params_}")
        print(f"Best CV ROC-AUC: {grid.best_score_:.4f}")
        
        # Evaluate on test set
        y_pred = grid.predict(X_test)
        y_proba = grid.predict_proba(X_test)[:, 1] if hasattr(grid, 'predict_proba') else None
        metrics = evaluate(y_test, y_pred, y_proba)
        print(f"Test Accuracy: {metrics['accuracy']:.4f}")
        
        if grid.best_score_ > best_score:
            best_score = grid.best_score_
            best_estimator = grid.best_estimator_
            best_model_name = model_name
    
    # 5. Save best model
    if best_estimator:
        model_path = os.path.join(MODELS_DIR, f"{dataset_name}_model.pkl")
        save_model(best_estimator, model_path)
        print(f"\n✅ Best model ({best_model_name}) saved to {model_path}")
        print(f"Best CV ROC-AUC: {best_score:.4f}")
    else:
        print("No model was trained successfully.")
    
    return best_estimator