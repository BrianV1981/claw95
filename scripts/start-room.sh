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

python3 -m src.server --policy config/policy.yaml &
SERVER_PID=$!

sleep 1

# agent_bridge reads CLAW95_TOKEN from env automatically if set.
python3 src/agent_bridge.py --name AgentA &
A_PID=$!
python3 src/agent_bridge.py --name AgentB &
B_PID=$!

echo "Claw95 room started. PIDs: server=$SERVER_PID a=$A_PID b=$B_PID"
echo "Press Ctrl+C to stop all."

wait
