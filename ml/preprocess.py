import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

def get_preprocessor(dataset_name, config):
    """Return a ColumnTransformer that applies scaling and imputation."""
    
    num_feats = config['numerical_features']
    cat_feats = config.get('categorical_features', [])
    
    # Numerical pipeline
    num_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler() if config.get('scaler') == 'standard' else MinMaxScaler())
    ])
    
    # Categorical pipeline
    cat_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    transformers = []
    if num_feats:
        transformers.append(('num', num_pipeline, num_feats))
    if cat_feats:
        transformers.append(('cat', cat_pipeline, cat_feats))
    
    preprocessor = ColumnTransformer(transformers)
    return preprocessor

def clean_diabetes(df, config):
    """Replace 0 with median only if columns are listed in config."""
    df_clean = df.copy()
    zero_cols = config.get('zero_to_median', [])
    if not zero_cols:
        return df_clean                      # nothing to do
    for col in zero_cols:
        if col not in df_clean.columns:
            print(f"⚠️ Warning: Column '{col}' not found. Skipping zero replacement.")
            continue
        non_zero = df_clean[col] != 0
        if non_zero.sum() == 0:
            print(f"⚠️ Warning: All values in '{col}' are zero. Cannot compute median.")
            continue
        median_val = df_clean.loc[non_zero, col].median()
        df_clean[col] = df_clean[col].replace(0, median_val)
    return df_clean

def clean_heart(df, config):
    """Handle missing values in 'ca' and 'thal'."""
    df_clean = df.copy()
    df_clean = df_clean.replace('?', np.nan)
    
    if 'ca' in df_clean.columns:
        df_clean['ca'] = pd.to_numeric(df_clean['ca'], errors='coerce')
    if 'thal' in df_clean.columns:
        df_clean['thal'] = pd.to_numeric(df_clean['thal'], errors='coerce')
    
    return df_clean

def load_and_clean(dataset_name, config):
    """Load CSV, normalise column names to lowercase, and apply dataset-specific cleaning."""
    df = pd.read_csv(config['file_path'])

    # --- DEBUG: Show column names BEFORE any processing ---
    print(f"\n📁 Dataset: {dataset_name}")
    print(f"Original columns: {df.columns.tolist()}")
    
    # Normalise: lowercase, strip spaces
    df.columns = df.columns.str.strip().str.lower()
    print(f"Normalised columns: {df.columns.tolist()}")
    # ------------------------------------------------------
    
    df.columns = df.columns.str.lower()
    
    if dataset_name == 'diabetes':
        df = clean_diabetes(df, config)
    elif dataset_name == 'heart':
        df = clean_heart(df, config)
    return df