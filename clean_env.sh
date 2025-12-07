#!/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Cleaning virtual environments, logs, and background demo processes in $ROOT_DIR"

# Kill processes by PID files (if present)
LOG_DIR="$ROOT_DIR/logs"
if [ -d "$LOG_DIR" ]; then
  for pidfile in "$LOG_DIR"/*.pid; do
    [ -f "$pidfile" ] || continue
    PID=$(cat "$pidfile" 2>/dev/null || true)
    if [ -n "$PID" ]; then
      if ps -p "$PID" > /dev/null 2>&1; then
        echo "Killing PID $PID"
        kill "$PID" || true
      fi
    fi
    rm -f "$pidfile"
  done
fi

# Also attempt to pkill common commands started by run_all.sh
echo "Attempting to pkill background demo processes (flask, streamlit, python producer/consumer)..."
pkill -f "flask run" 2>/dev/null || true
pkill -f "streamlit" 2>/dev/null || true
pkill -f "producer.py" 2>/dev/null || true
pkill -f "consumer.py" 2>/dev/null || true

# Remove venv directories (prompt)
read -p "Remove all 'venv' virtual env folders under project subdirectories? [y/N]: " CONF
if [[ "$CONF" =~ ^[Yy]$ ]]; then
  find "$ROOT_DIR" -type d -name "venv" -prune -print -exec rm -rf {} \;
  echo "Removed venv directories."
else
  echo "Skipped removing venvs."
fi

# Clear logs (prompt)
read -p "Remove logs directory at $LOG_DIR? [y/N]: " CONF2
if [[ "$CONF2" =~ ^[Yy]$ ]]; then
  rm -rf "$LOG_DIR"
  echo "Logs removed."
else
  echo "Skipped log removal."
fi

echo "Cleanup complete."
