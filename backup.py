# backup.py
# ----------

import os
import boto3
from datetime import datetime
from config import BUCKET_NAME, S3_PREFIX, SOURCE_FOLDER

def create_s3_client():
    return boto3.client(
        "s3",
        region_name="us-east-1"
    )

def generate_job_id():
    """Create a unique ID for this backup job using current time."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def upload_file(s3_client, local_path, s3_key, extra_metadata=None):
    """
    Upload one file to S3 and attach custom metadata.
    """
    extra_args = {}
    if extra_metadata:
        # S3 user metadata must start with x-amz-meta-
        extra_args["Metadata"] = {f"x-amz-meta-{k}": str(v) for k, v in extra_metadata.items()}

    s3_client.upload_file(
        Filename=local_path,
        Bucket=BUCKET_NAME,
        Key=s3_key,
        ExtraArgs=extra_args
    )

def run_backup():
    """
    Main function: upload all files from SOURCE_FOLDER to S3.
    Returns a dictionary with job information.
    """
    s3 = create_s3_client()
    job_id = generate_job_id()
    uploaded_files = []
    total_size = 0
    success = True
    error_message = ""

    print(f"Starting backup job: {job_id}")

    try:
        for root, dirs, files in os.walk(SOURCE_FOLDER):
            for filename in files:
                local_path = os.path.join(root, filename)

                # Create a clean S3 key
                relative_path = os.path.relpath(local_path, SOURCE_FOLDER)
                s3_key = f"{S3_PREFIX}{job_id}/{relative_path}".replace("\\", "/")

                # Get file size and modification time
                file_size = os.path.getsize(local_path)
                mtime = os.path.getmtime(local_path)

                metadata = {
                    "job-id": job_id,
                    "original-mtime": str(mtime),
                    "file-size": str(file_size)
                }

                upload_file(s3, local_path, s3_key, metadata)

                uploaded_files.append({
                    "local_path": local_path,
                    "s3_key": s3_key,
                    "size": file_size
                })
                total_size += file_size
                print(f"  Uploaded: {relative_path}")

    except Exception as e:
        success = False
        error_message = str(e)
        print(f"Backup failed: {e}")

    result = {
        "job_id": job_id,
        "success": success,
        "error_message": error_message,
        "num_files": len(uploaded_files),
        "total_size": total_size,
        "uploaded_files": uploaded_files,
        "timestamp": datetime.now().isoformat()
    }

    return result