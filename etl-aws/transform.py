# transform.py
import pandas as pd

def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    # Example transformations: normalize column names, drop NA, dedupe, cast types
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    if "id" in df.columns:
        df.drop_duplicates(subset=["id"], inplace=True)
    df.fillna("", inplace=True)
    # Example: cast numeric columns safely
    for col in df.select_dtypes(include=["float", "int"]).columns:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df
