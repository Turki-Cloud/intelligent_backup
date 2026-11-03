# features.py
# ------------

import pandas as pd
import numpy as np
from config import HISTORY_FILE

def load_history():
    """Read the history CSV and parse dates."""
    df = pd.read_csv(HISTORY_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def create_features(df):
    """
    Create useful features for anomaly detection.
    """
    df = df.copy()

    # Size change compared to previous backup
    df["size_delta"] = df["total_size"].diff().fillna(0)
    df["size_pct_change"] = df["total_size"].pct_change().fillna(0) * 100

    # Number of files change
    df["files_delta"] = df["num_files"].diff().fillna(0)

    # Hours since previous backup
    df["hours_since_last"] = df["timestamp"].diff().dt.total_seconds().fillna(0) / 3600

    # Success as 0 or 1
    df["success_flag"] = df["success"].astype(int)

    # Rolling statistics (last 5 backups)
    df["size_rolling_mean"] = df["total_size"].rolling(window=5, min_periods=1).mean()
    df["size_rolling_std"] = df["total_size"].rolling(window=5, min_periods=1).std().fillna(0)

    # Select only the columns we will give to the model
    feature_cols = [
        "total_size", "num_files", "size_delta", "size_pct_change",
        "files_delta", "hours_since_last", "success_flag",
        "size_rolling_mean", "size_rolling_std"
    ]

    return df[feature_cols].fillna(0)