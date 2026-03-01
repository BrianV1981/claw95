#!/usr/bin/env bash
set -euo pipefail

# One-command interactive stack using tmux.
# Creates a 2x2 session with 4 panes:
#   pane 0: server
#   pane 1: OpenClaw subagent bridge
#   pane 2: interactive user client
#   pane 3: log tail

SESSION="${CLAW95_SESSION:-claw95}"
PORT="${CLAW95_PORT:-8765}"

cd "$(dirname "$0")/.."

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is required. Install with: sudo apt install tmux"
  exit 1
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session '$SESSION' already exists. Attach with: tmux attach -t $SESSION"
  exit 1
fi

if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -e .[dev] >/dev/null

if ss -H -lnt "sport = :$PORT" | grep -q ":$PORT"; then
  echo "Port $PORT is already in use. Stop existing server or set CLAW95_PORT."
  exit 1
fi

ROOT="$(pwd)"
VENV_ACT="$ROOT/.venv/bin/activate"

# Create session and panes
_tmux_cmd() {
  tmux send-keys -t "$SESSION:$1" "$2" C-m
}

tmux new-session -d -s "$SESSION" -n room

# Pane 0: server
_tmux_cmd "room.0" "cd '$ROOT' && source '$VENV_ACT' && python3 -m src.server --port $PORT --policy config/policy.yaml"

# Pane 1: bridge
 tmux split-window -h -t "$SESSION:room.0"
_tmux_cmd "room.1" "cd '$ROOT' && source '$VENV_ACT' && while true; do python3 -m src.openclaw_subagent_bridge --config config/subagent_bridge.yaml || true; echo '[bridge] reconnecting in 2s...'; sleep 2; done"

# Pane 2: interactive user client
 tmux split-window -v -t "$SESSION:room.0"
_tmux_cmd "room.2" "cd '$ROOT' && source '$VENV_ACT' && python3 src/agent_bridge.py --name User --uri ws://127.0.0.1:$PORT"

# Pane 3: logs tail
 tmux split-window -v -t "$SESSION:room.1"
_tmux_cmd "room.3" "cd '$ROOT' && tail -f logs/events.jsonl logs/transcript.md"

# Nice 2x2 layout
 tmux select-layout -t "$SESSION:room" tiled

echo "Started tmux session '$SESSION' on port $PORT"
echo "Attach: tmux attach -t $SESSION"
echo "Stop:   ./scripts/dev-stack-stop.sh ${SESSION}"
