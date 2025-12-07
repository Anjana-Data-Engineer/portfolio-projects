#!/bin/bash
set -euo pipefail

# Run demos for local development. Outputs go to logs/<service>.log
# Usage: ./run_all.sh
# Stop processes: run `pkill -f "flask.*app.py"` or `pkill -f streamlit` or use clean_env.sh to kill background jobs.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

echo "Starting demo services... logs -> $LOG_DIR"

# Helper to run a command in background and save PID
run_bg() {
  NAME="$1"
  shift
  CMD="$@"
  LOG="$LOG_DIR/$NAME.log"

  echo "Launching $NAME..."
  nohup bash -lc "$CMD" > "$LOG" 2>&1 &
  PID=$!
  echo "$NAME PID: $PID" > "$LOG_DIR/$NAME.pid"
  echo "$NAME started (PID $PID), log: $LOG"
}

# 1) Flask API
if [ -d "$ROOT_DIR/flask-api" ]; then
  run_bg "flask-api" "cd '$ROOT_DIR/flask-api' && source venv/bin/activate >/dev/null 2>&1 || true && \
    export FLASK_APP=app.py && flask run --host=0.0.0.0 --port=8000"
else
  echo "flask-api folder not found; skipping."
fi

# 2) Finance Dashboard (Streamlit)
if [ -d "$ROOT_DIR/finance-dashboard" ]; then
  run_bg "finance-dashboard" "cd '$ROOT_DIR/finance-dashboard' && source venv/bin/activate >/dev/null 2>&1 || true && \
    streamlit run app.py --server.port 8501 --server.headless true"
else
  echo "finance-dashboard folder not found; skipping."
fi

# 3) Log producer (simulated)
if [ -d "$ROOT_DIR/log-monitor" ]; then
  run_bg "log-producer" "cd '$ROOT_DIR/log-monitor' && source venv/bin/activate >/dev/null 2>&1 || true && \
    python producer.py"
  run_bg "log-consumer" "cd '$ROOT_DIR/log-monitor' && source venv/bin/activate >/dev/null 2>&1 || true && \
    python consumer.py"
else
  echo "log-monitor folder not found; skipping."
fi

# 4) Data quality sample run (one-off)
if [ -d "$ROOT_DIR/data-quality" ]; then
  if [ -f "$ROOT_DIR/data-quality/sample.csv" ]; then
    echo "Running data-quality sample check (one-off)..."
    (cd "$ROOT_DIR/data-quality" && source venv/bin/activate >/dev/null 2>&1 || true && \
      python dq_engine.py --file sample.csv --rules rules/sample_rules.yaml) || true
  else
    echo "No sample.csv in data-quality; skip sample run."
  fi
fi

echo "All requested services started. To see logs: ls $LOG_DIR/*.log"
echo "To stop all background processes started by this script, run: ./clean_env.sh"
