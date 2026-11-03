# report.py
# ----------

import pandas as pd
from datetime import datetime
from config import HISTORY_FILE
import os

def generate_health_report(anomaly_score=None, risk_level=None, reasons=None):
    """
    Create both a text report and a nice HTML dashboard.
    Now also shows Anomaly Score and Risk Level.
    """

    if not os.path.exists(HISTORY_FILE):
        print("No history file found yet.")
        return

    df = pd.read_csv(HISTORY_FILE)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    total_jobs = len(df)
    successful = int(df["success"].sum())
    failed = total_jobs - successful
    success_rate = (successful / total_jobs * 100) if total_jobs > 0 else 0
    latest_size_mb = df["total_size"].iloc[-1] / (1024 * 1024) if total_jobs > 0 else 0

    # ---------- Text Report ----------
    text_report = f"""
=====================================
   BACKUP HEALTH REPORT
   Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
=====================================
Total backup jobs : {total_jobs}
Successful        : {successful}
Failed            : {failed}
Success rate      : {success_rate:.1f}%
Latest backup size: {latest_size_mb:.2f} MB
"""

    if anomaly_score is not None:
        text_report += f"""
Anomaly Score     : {anomaly_score:.3f}
Risk Level        : {risk_level}
Reasons           : {reasons if reasons else 'N/A'}
"""

    print(text_report)

    with open("data/health_report.txt", "w", encoding="utf-8") as f:
        f.write(text_report)

    # ---------- Prepare anomaly card color ----------
    if risk_level == "Critical":
        risk_color = "#e53935"      # red
        risk_bg = "#ffebee"
    elif risk_level == "Warning":
        risk_color = "#fb8c00"      # orange
        risk_bg = "#fff3e0"
    elif risk_level == "Normal":
        risk_color = "#43a047"      # green
        risk_bg = "#e8f5e9"
    else:
        risk_color = "#1a73e8"
        risk_bg = "#e8f0fe"
        risk_level = "Not available yet"
        anomaly_score = 0.0

    # ---------- HTML rows for recent jobs ----------
    rows_html = ""
    for _, row in df.tail(10).iterrows():
        status = "✅ OK" if row["success"] else "❌ FAILED"
        size_mb = row["total_size"] / (1024 * 1024)
        rows_html += f"""
        <tr>
            <td>{row['job_id']}</td>
            <td>{row['timestamp']}</td>
            <td>{status}</td>
            <td>{row['num_files']}</td>
            <td>{size_mb:.2f} MB</td>
        </tr>
        """

    # ---------- Full HTML ----------
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Intelligent Backup Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f4f6f9;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1050px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #1a73e8;
            text-align: center;
            margin-bottom: 5px;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}
        .cards {{
            display: flex;
            gap: 15px;
            margin: 25px 0;
            flex-wrap: wrap;
        }}
        .card {{
            flex: 1;
            min-width: 160px;
            background: #e8f0fe;
            padding: 18px;
            border-radius: 10px;
            text-align: center;
        }}
        .card h3 {{
            margin: 0;
            font-size: 14px;
            color: #555;
        }}
        .card p {{
            font-size: 26px;
            font-weight: bold;
            margin: 8px 0 0;
            color: #1a73e8;
        }}
        .anomaly-card {{
            background: {risk_bg};
            border: 2px solid {risk_color};
        }}
        .anomaly-card p {{
            color: {risk_color};
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background: #1a73e8;
            color: white;
        }}
        tr:hover {{
            background: #f1f5fb;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #888;
            font-size: 14px;
        }}
        .reasons {{
            margin-top: 8px;
            font-size: 13px;
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Intelligent Backup Management Dashboard</h1>
        <p class="subtitle">AWS S3 + Artificial Intelligence Anomaly Detection</p>

        <div class="cards">
            <div class="card">
                <h3>Total Jobs</h3>
                <p>{total_jobs}</p>
            </div>
            <div class="card">
                <h3>Successful</h3>
                <p>{successful}</p>
            </div>
            <div class="card">
                <h3>Failed</h3>
                <p>{failed}</p>
            </div>
            <div class="card">
                <h3>Success Rate</h3>
                <p>{success_rate:.1f}%</p>
            </div>
            <div class="card">
                <h3>Latest Size</h3>
                <p>{latest_size_mb:.1f} MB</p>
            </div>
            <div class="card anomaly-card">
                <h3>Anomaly Score</h3>
                <p>{f'{anomaly_score:.3f}' if isinstance(anomaly_score, (int, float)) and anomaly_score is not None else 'N/A'}</p>
                <div class="reasons"><strong>{risk_level}</strong></div>
            </div>
        </div>

        <h2>Recent Backup Jobs</h2>
        <table>
            <thead>
                <tr>
                    <th>Job ID</th>
                    <th>Timestamp</th>
                    <th>Status</th>
                    <th>Files</th>
                    <th>Size</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

        <div class="footer">
            Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |
            Intelligent Backup System using AWS S3 + AI
        </div>
    </div>
</body>
</html>
"""

    os.makedirs("data", exist_ok=True)
    with open("data/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("HTML dashboard saved to: data/index.html")
    return text_report