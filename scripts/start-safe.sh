#!/usr/bin/env bash
set -euo pipefail

# Minimal, reliable launcher: starts SERVER ONLY and prints exact client commands.
# Use this when tmux/panes feel funky.

PORT="${CLAW95_PORT:-8765}"

cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -e .[dev] >/dev/null

if ss -H -lnt "sport = :$PORT" | grep -q ":$PORT"; then
  echo "Port $PORT is already in use. Stop existing server or set CLAW95_PORT."
  exit 1
fi

echo "Starting server on ws://127.0.0.1:$PORT ..."
python3 -m src.server --port "$PORT" --policy config/policy.yaml &
SERVER_PID=$!

cleanup(){
  kill "$SERVER_PID" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

sleep 1
if ! kill -0 "$SERVER_PID" 2>/dev/null; then
  echo "Server failed to start."
  exit 1
fi

cat <<MSG

✅ Server running (pid=$SERVER_PID)

Open TWO new terminals and run exactly:

Terminal B:
  cd ~/claw95
  ./scripts/start-client.sh AgentA ws://127.0.0.1:$PORT

Terminal C:
  cd ~/claw95
  ./scripts/start-client.sh AgentB ws://127.0.0.1:$PORT

Press Ctrl+C here to stop server.
MSG

wait "$SERVER_PID"
