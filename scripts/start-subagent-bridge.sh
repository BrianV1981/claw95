#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
source .venv/bin/activate 2>/dev/null || true
exec python3 -m src.openclaw_subagent_bridge --config config/subagent_bridge.yaml
