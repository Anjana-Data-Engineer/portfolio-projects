import os
import io
import json
import boto3
import pandas as pd
from sqlalchemy import create_engine

s3 = boto3.client("s3")

# env vars (set in Lambda)
RDS_URL = os.environ.get("RDS_URL")  # postgresql://user:pass@host:port/db
TARGET_TABLE = os.environ.get("TARGET_TABLE", "ingested_data")

def lambda_handler(event, context):
    # Event from S3 put
    for rec in event.get("Records", []):
        bucket = rec["s3"]["bucket"]["name"]
        key = rec["s3"]["object"]["key"]
        resp = s3.get_object(Bucket=bucket, Key=key)
        content = resp["Body"].read()
        # assume csv for demo
        df = pd.read_csv(io.BytesIO(content))
        df = transform_df(df)
        engine = create_engine(RDS_URL)
        df.to_sql(TARGET_TABLE, con=engine, if_exists="append", index=False)
    return {"status": "ok"}

#3️ Lambda processes data

# Reads the file from S3
#Parses data using pandas
#Cleans/validates (duplicates removal, null handling)
#Transforms data
#Inserts into PostgreSQL using SQLAlchemy

#4️ Logs and metrics captured

#CloudWatch captures:
#Processing time
#Number of rows loaded
#Errors / exceptions
