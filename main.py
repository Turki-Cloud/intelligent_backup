# main.py
# --------

from backup import run_backup
from metadata import save_metadata
from features import load_history, create_features
from anomaly_model import train_model, load_model, get_anomaly_score, classify_risk
from alert import send_alert
from report import generate_health_report
from config import MIN_TRAINING_SAMPLES
import numpy as np

def main():
    print("=" * 50)
    print("Intelligent Backup Management System")
    print("=" * 50)

    # 1. Run the backup
    backup_result = run_backup()

    # 2. Save metadata
    save_metadata(backup_result)

    # 3. Load history and create features
    history = load_history()
    features_df = create_features(history)

    # 4. Train model if we have enough data and no model yet
    model = load_model()
    if model is None and len(history) >= MIN_TRAINING_SAMPLES:
        model = train_model()

        # 5. Score the latest backup
    anomaly_score = None
    risk_level = None
    reasons_text = None

    if model is not None and len(features_df) > 0:
        latest_features = features_df.iloc[[-1]]
        anomaly_score = get_anomaly_score(model, latest_features)
        risk_level = classify_risk(anomaly_score)

        print(f"\nAnomaly Score : {anomaly_score:.3f}")
        print(f"Risk Level    : {risk_level}")

        reasons = []
        if latest_features["size_pct_change"].values[0] > 100:
            reasons.append("Sudden large size increase")
        if latest_features["files_delta"].values[0] > 500:
            reasons.append("Very high number of changed files")
        if latest_features["success_flag"].values[0] == 0:
            reasons.append("Backup failed")
        if not reasons:
            reasons.append("Unusual pattern detected by AI model")

        reasons_text = ", ".join(reasons)

        # Send alert if needed
        send_alert(
            job_id=backup_result["job_id"],
            risk_level=risk_level,
            score=anomaly_score,
            reasons=reasons_text
        )
    else:
        print("Not enough data yet for anomaly detection.")

    # 7. Generate health report (now with AI results)
    generate_health_report(
        anomaly_score=anomaly_score,
        risk_level=risk_level,
        reasons=reasons_text
    )

    print("\nPipeline finished successfully.")

if __name__ == "__main__":
    main()