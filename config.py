# config.py
# ----------
# This file contains all the settings for the project.

import os
import boto3

# AWS S3 bucket name (change this to your real bucket name)
BUCKET_NAME = "xxxxxxx"   # ← change this

# Folder inside the bucket where backups will be stored
S3_PREFIX = "backups/"

# Local folder that contains the files you want to backup
SOURCE_FOLDER = "sample_data/"

# Where we store the history of all backups
HISTORY_FILE = "data/history.csv"

# Where we save the trained AI model
MODEL_FILE = "data/model.joblib"

# SNS Topic ARN for sending alerts (get this from AWS SNS console)
SNS_TOPIC_ARN = "xxxxxxx"  # ← change this

# Risk thresholds
WARNING_THRESHOLD = 0.65    # score above this = Warning
CRITICAL_THRESHOLD = 0.85   # score above this = Critical

# Minimum number of normal backups needed before training the model
MIN_TRAINING_SAMPLES = 15