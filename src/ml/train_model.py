import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import xgboost as xgb

def generate_synthetic_training_data(num_samples: int = 10000) -> pd.DataFrame:
    """Generates synthetic banking loan dataset for demonstration and training."""
    np.random.seed(42)
    dti = np.random.uniform(0.1, 0.9, num_samples)
    ltv = np.random.uniform(0.2, 1.2, num_samples)
    p_instances = np.random.poisson(lam=1.0, size=num_samples)
    
    # Target definition based on risk logic + some noise
    risk_score = (0.40 * dti) + (0.35 * ltv) + (0.25 * (p_instances / 5.0))
    default_target = (risk_score > 0.55).astype(int)
    
    df = pd.DataFrame({
        "dti": dti,
        "ltv": ltv,
        "p_instances": p_instances,
        "default": default_target
    })
    return df

def train_risk_model(model_output_path: str = "src/ml/risk_xgboost_model.pkl"):
    """Trains an XGBoost model to predict loan default risk."""
    print("Generating training dataset...")
    df = generate_synthetic_training_data()
    
    X = df[["dti", "ltv", "p_instances"]]
    y = df["default"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluation
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    print("\n--- Model Evaluation Metrics ---")
    print(classification_report(y_test, preds))
    print(f"ROC-AUC Score: {roc_auc_score(y_test, probs):.4f}")
    
    # Save model artifact
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f"\nModel successfully saved to {model_output_path}")

if __name__ == "__main__":
    train_risk_model()
