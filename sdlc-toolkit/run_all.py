# run_all.py
import subprocess, sys

CHECKS = [
    "python -m checks.check_docs",
    "python -m checks.check_lint",
    "python -m checks.check_tests",
]

def run_cmd(cmd):
    print(">>>", cmd)
    return subprocess.call(cmd, shell=True)

def main():
    failed = []
    for c in CHECKS:
        rc = run_cmd(c)
        if rc != 0:
            failed.append((c, rc))
    if failed:
        print("Failed checks:", failed)
        sys.exit(1)
    print("All checks passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
