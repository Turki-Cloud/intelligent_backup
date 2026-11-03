# anomaly_model.py
# -----------------

import os
import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest
from config import MODEL_FILE, MIN_TRAINING_SAMPLES, WARNING_THRESHOLD, CRITICAL_THRESHOLD
from features import load_history, create_features

def train_model():
    """Train Isolation Forest on historical normal data."""
    df = load_history()

    if len(df) < MIN_TRAINING_SAMPLES:
        print(f"Not enough data to train (need at least {MIN_TRAINING_SAMPLES}).")
        return None

    features = create_features(df)

    # IsolationForest: lower score = more anomalous (we will invert it later)
    model = IsolationForest(
        n_estimators=100,
        contamination=0.08,   # expect about 8% anomalies
        random_state=42
    )
    model.fit(features)

    # Save the trained model
    os.makedirs(os.path.dirname(MODEL_FILE), exist_ok=True)
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved.")
    return model

def load_model():
    """Load the saved model from disk."""
    if os.path.exists(MODEL_FILE):
        return joblib.load(MODEL_FILE)
    return None

def get_anomaly_score(model, latest_features):
    """
    Return a score between 0 and 1.
    Higher score = more anomalous.
    """
    # decision_function: higher = more normal → we invert it
    raw_score = model.decision_function(latest_features)[0]
    # Convert to 0–1 range (simple normalization)
    score = 1 / (1 + np.exp(raw_score * 3))   # sigmoid-like
    return float(score)

def classify_risk(score):
    """Convert numeric score into risk level."""
    if score >= CRITICAL_THRESHOLD:
        return "Critical"
    elif score >= WARNING_THRESHOLD:
        return "Warning"
    else:
        return "Normal"