#!/usr/bin/env sh
set -eu

PROJECT_DIR="/home/patolizo/Documents/GitHub/CanadaTracker"
cd "$PROJECT_DIR"

if [ -x "$PROJECT_DIR/.venv/bin/python" ]; then
  exec "$PROJECT_DIR/.venv/bin/python" "$PROJECT_DIR/main.py"
fi

exec python3 "$PROJECT_DIR/main.py"
