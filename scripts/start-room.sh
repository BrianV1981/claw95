#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -e .[dev] >/dev/null

cleanup() {
  jobs -p | xargs -r kill >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

PORT="${CLAW95_PORT:-8765}"

if ss -H -lnt "sport = :$PORT" | grep -q ":$PORT"; then
  echo "Port $PORT already in use. Stop existing server or set CLAW95_PORT."
  exit 1
fi

python3 -m src.server --port "$PORT" --policy config/policy.yaml &
SERVER_PID=$!

sleep 1
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "Server failed to start. Check logs/output above."
  exit 1
fi

URI="ws://127.0.0.1:$PORT"

# agent_bridge reads CLAW95_TOKEN from env automatically if set.
python3 src/agent_bridge.py --name AgentA --uri "$URI" --no-input &
A_PID=$!
python3 src/agent_bridge.py --name AgentB --uri "$URI" --no-input &
B_PID=$!

echo "Claw95 room started. PIDs: server=$SERVER_PID a=$A_PID b=$B_PID on $URI"
echo "Press Ctrl+C to stop all."

wait
