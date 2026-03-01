#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[preflight] repo: $(pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[preflight] FAIL: python3 not found"
  exit 1
fi

echo "[preflight] python: $(python3 --version)"

if [[ ! -d .venv ]]; then
  echo "[preflight] INFO: .venv missing; creating..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -e .[dev] >/dev/null

echo "[preflight] checking policy file..."
if [[ ! -f config/policy.yaml ]]; then
  echo "[preflight] FAIL: config/policy.yaml missing"
  exit 1
fi

echo "[preflight] checking port availability (8765)..."
if ss -H -lnt "sport = :8765" | grep -q 8765; then
  echo "[preflight] WARN: port 8765 already in use"
else
  echo "[preflight] OK: port 8765 free"
fi

echo "[preflight] running quick checks..."
ruff check . >/dev/null
mypy src tests scripts >/dev/null
pytest -q >/dev/null

echo "[preflight] PASS"
