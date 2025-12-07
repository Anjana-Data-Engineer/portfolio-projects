# dq_engine.py
import argparse
import pandas as pd
import yaml
from utils import load_rules, print_results

def run_checks(df: pd.DataFrame, rules: dict):
    results = []
    for rule in rules.get("checks", []):
        typ = rule.get("type")
        col = rule.get("column")
        name = rule.get("name", f"{typ}:{col}")
        if typ == "not_null":
            missing = df[col].isnull().sum()
            ok = missing == 0
            results.append((name, ok, {"missing": int(missing)}))
        elif typ == "unique":
            dup = df.duplicated(subset=[col]).sum()
            ok = dup == 0
            results.append((name, ok, {"duplicates": int(dup)}))
        elif typ == "range":
            lo, hi = rule["min"], rule["max"]
            out = ((df[col] < lo) | (df[col] > hi)).sum()
            ok = out == 0
            results.append((name, ok, {"out_of_range": int(out)}))
        elif typ == "regex":
            import re
            pattern = re.compile(rule["pattern"])
            invalid = df[~df[col].astype(str).apply(lambda x: bool(pattern.match(x)))]
            ok = invalid.empty
            results.append((name, ok, {"invalid_count": int(len(invalid))}))
        else:
            results.append((name, False, {"error":"unknown check type"}))
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--rules", required=True)
    args = parser.parse_args()
    df = pd.read_csv(args.file)
    rules = load_rules(args.rules)
    res = run_checks(df, rules)
    print_results(res)
    exit(0 if all(ok for _, ok, _ in res) else 1)
