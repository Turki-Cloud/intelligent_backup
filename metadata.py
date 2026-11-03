# metadata.py
# ------------

import os
import pandas as pd
from datetime import datetime
from config import HISTORY_FILE

def ensure_history_file():
    """Create the history CSV with headers if it does not exist."""
    if not os.path.exists(HISTORY_FILE):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        df = pd.DataFrame(columns=[
            "job_id", "timestamp", "success", "num_files",
            "total_size", "error_message"
        ])
        df.to_csv(HISTORY_FILE, index=False)

def save_metadata(backup_result):
    """
    Append one new row of metadata to the history file.
    """
    ensure_history_file()

    new_row = {
        "job_id": backup_result["job_id"],
        "timestamp": backup_result["timestamp"],
        "success": backup_result["success"],
        "num_files": backup_result["num_files"],
        "total_size": backup_result["total_size"],
        "error_message": backup_result.get("error_message", "")
    }

    df = pd.read_csv(HISTORY_FILE)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

    print(f"Metadata saved for job {backup_result['job_id']}")
    return new_row