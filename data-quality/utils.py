# utils.py
import yaml

def load_rules(path):
    with open(path) as f:
        return yaml.safe_load(f)

def print_results(results):
    for name, ok, info in results:
        status = "OK" if ok else "FAIL"
        print(f"{name}: {status} — {info}")
