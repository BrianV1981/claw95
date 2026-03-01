#!/usr/bin/env bash
set -euo pipefail
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <AgentName> [ws_url]"
  exit 1
fi

NAME="$1"
URL="${2:-ws://127.0.0.1:8765}"

cd "$(dirname "$0")/.."
source .venv/bin/activate
exec python3 src/agent_bridge.py --name "$NAME" --uri "$URL"
