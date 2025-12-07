# local_etl_test.py
import argparse
import os
import pandas as pd
from transform import transform_df
from sqlalchemy import create_engine

def run_local(file, db_url, table="ingested_data"):
    df = pd.read_csv(file)
    df = transform_df(df)
    engine = create_engine(db_url)
    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"Inserted {len(df)} rows into {table}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--db", required=True, help="SQLAlchemy DB URL (sqlite:// or postgres URL)")
    args = ap.parse_args()
    run_local(args.file, args.db)
