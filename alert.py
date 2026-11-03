# alert.py
# ---------

import boto3
from config import SNS_TOPIC_ARN

def send_alert(job_id, risk_level, score, reasons):
    """Publish an alert message to SNS."""
    if risk_level == "Normal":
        return  # no need to alert

    sns = boto3.client("sns")

    message = f"""
Backup Anomaly Alert
--------------------
Job ID     : {job_id}
Risk Level : {risk_level}
Score      : {score:.3f}
Reasons    : {reasons}

Please investigate the backup.
"""
    subject = f"[{risk_level}] Backup Anomaly Detected - {job_id}"

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message
    )
    print(f"Alert sent: {risk_level}")