# lambda_function.py
import os
import io
import json
import boto3
import pandas as pd
from sqlalchemy import create_engine
from transform import transform_df

s3 = boto3.client("s3")
RDS_URL = os.environ.get("RDS_URL")  # e.g. postgresql://user:pass@host:5432/db
TARGET_TABLE = os.environ.get("TARGET_TABLE", "ingested_data")
CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", "500"))

def read_s3_csv(bucket, key):
    resp = s3.get_object(Bucket=bucket, Key=key)
    data = resp["Body"].read()
    return pd.read_csv(io.BytesIO(data))

def to_postgres(df: pd.DataFrame):
    engine = create_engine(RDS_URL)
    df.to_sql(TARGET_TABLE, engine, if_exists="append", index=False, method="multi", chunksize=CHUNK_SIZE)

def lambda_handler(event, context):
    results = []
    for rec in event.get("Records", []):
        bucket = rec["s3"]["bucket"]["name"]
        key = rec["s3"]["object"]["key"]
        try:
            df = read_s3_csv(bucket, key)
            df = transform_df(df)
            if not df.empty:
                to_postgres(df)
            results.append({"key": key, "status": "ok", "rows": len(df)})
        except Exception as e:
            results.append({"key": key, "status": "error", "error": str(e)})
    return {"results": results}
