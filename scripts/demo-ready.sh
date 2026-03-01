#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

source .venv/bin/activate 2>/dev/null || true

echo "[demo-ready] preflight..."
./scripts/preflight.sh

echo "[demo-ready] doctor..."
./scripts/doctor.sh

echo "[demo-ready] starting temporary server for smoke test..."
python3 -m src.server --policy config/policy.yaml >/tmp/claw95-demo-server.log 2>&1 &
SERVER_PID=$!
cleanup(){
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

sleep 1

echo "[demo-ready] smoke test..."
python3 scripts/smoke_test.py

echo "[demo-ready] PASS"
