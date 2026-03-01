#!/usr/bin/env bash
set -euo pipefail

# Two-tab tmux stack:
# - Tab 1 (server): Claw95 server
# - Tab 2 (chat): 4 panes -> User + OpsBot + QABot + GrowthBot (OpenClaw subagent bridges)

SESSION="${CLAW95_SESSION:-claw95-2tab}"
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
TMP_CFG_DIR="$ROOT/.runtime"
mkdir -p "$TMP_CFG_DIR"

cat > "$TMP_CFG_DIR/bridge_ops.yaml" <<YAML
enabled: true
room_uri: "ws://127.0.0.1:$PORT"
bridge_name: "OpsBot"
trigger_mode: "mention"
max_concurrent: 1
request_timeout_seconds: 120
session_mode: "room"
response_max_chars: 1200
agent_map:
  ops: "ops"
YAML

cat > "$TMP_CFG_DIR/bridge_qa.yaml" <<YAML
enabled: true
room_uri: "ws://127.0.0.1:$PORT"
bridge_name: "QABot"
trigger_mode: "mention"
max_concurrent: 1
request_timeout_seconds: 120
session_mode: "room"
response_max_chars: 1200
agent_map:
  qa: "reviewer"
YAML

cat > "$TMP_CFG_DIR/bridge_growth.yaml" <<YAML
enabled: true
room_uri: "ws://127.0.0.1:$PORT"
bridge_name: "GrowthBot"
trigger_mode: "mention"
max_concurrent: 1
request_timeout_seconds: 120
session_mode: "room"
response_max_chars: 1200
agent_map:
  growth: "growth"
YAML

_tmux_cmd() {
  tmux send-keys -t "$SESSION:$1" "$2" C-m
}

# Window 1: server
tmux new-session -d -s "$SESSION" -n server
_tmux_cmd "server.0" "cd '$ROOT' && source '$VENV_ACT' && python3 -m src.server --port $PORT --policy config/policy.yaml"

# Window 2: chat (4 panes)
tmux new-window -t "$SESSION" -n chat
_tmux_cmd "chat.0" "cd '$ROOT' && source '$VENV_ACT' && python3 src/agent_bridge.py --name User --uri ws://127.0.0.1:$PORT"

tmux split-window -h -t "$SESSION:chat.0"
_tmux_cmd "chat.1" "cd '$ROOT' && source '$VENV_ACT' && while true; do python3 -m src.openclaw_subagent_bridge --config '$TMP_CFG_DIR/bridge_ops.yaml' || true; echo '[OpsBot] reconnecting in 2s...'; sleep 2; done"

tmux split-window -v -t "$SESSION:chat.0"
_tmux_cmd "chat.2" "cd '$ROOT' && source '$VENV_ACT' && while true; do python3 -m src.openclaw_subagent_bridge --config '$TMP_CFG_DIR/bridge_qa.yaml' || true; echo '[QABot] reconnecting in 2s...'; sleep 2; done"

tmux split-window -v -t "$SESSION:chat.1"
_tmux_cmd "chat.3" "cd '$ROOT' && source '$VENV_ACT' && while true; do python3 -m src.openclaw_subagent_bridge --config '$TMP_CFG_DIR/bridge_growth.yaml' || true; echo '[GrowthBot] reconnecting in 2s...'; sleep 2; done"

tmux select-layout -t "$SESSION:chat" tiled

echo "Started tmux session '$SESSION'"
echo "Window 1: server"
echo "Window 2: chat (User + OpsBot + QABot + GrowthBot)"
echo "Attach: tmux attach -t $SESSION"
echo "Switch windows: Ctrl+b then n/p"
echo "Stop: tmux kill-session -t $SESSION"
