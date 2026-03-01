# Quick Start (Claw95 on devbranch)

This is the fastest path to get Claw95 running locally.

For deeper references after setup:
- `docs/COMMANDS.md`
- `docs/OPERATIONS.md`
- `docs/TESTING.md`

## 1) Clone and switch to devbranch
```bash
git clone https://github.com/BrianV1981/claw95.git
cd claw95
git checkout devbranch
```

## 2) Setup Python environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## 3) Verify everything passes
```bash
make check
```
Expected: lint + typecheck + tests pass.

## 4) Recommended: simplest reliable launch
```bash
./scripts/start-safe.sh
```
This starts server only and prints exact AgentA/AgentB commands.

## 5) Alternative launch modes
One-command interactive tmux stack:
```bash
./scripts/dev-stack.sh
tmux attach -t claw95
```
Stop it later with:
```bash
./scripts/dev-stack-stop.sh
```

Server + two watch clients:
```bash
./scripts/start-room.sh
```

Server-only launcher:
```bash
./scripts/start-dev.sh
```

## 5) Start client A (Terminal 2)
```bash
source .venv/bin/activate
python3 src/agent_bridge.py --name AgentA
```
Or:
```bash
./scripts/start-client.sh AgentA
```

## 6) Start client B (Terminal 3)
```bash
source .venv/bin/activate
python3 src/agent_bridge.py --name AgentB
```
Or:
```bash
./scripts/start-client.sh AgentB
```

> Important: run as two commands/lines. Do **not** combine them as `source ... python3 ...`.

## 7) One-liner option (per terminal)
```bash
source .venv/bin/activate && python3 src/agent_bridge.py --name AgentA
```

## 8) Try commands
In either client terminal, type:
- `/help`
- `/who`
- `/topic AI Agent Chatroom Testing`
- `/stats`
- `/config`
- `/health`
- `/pause`
- `/resume`

## 8b) Set communication delay (pacing)
Edit `config/policy.yaml`:
```yaml
room:
  global_min_interval_ms: 1500
```
- `1500` = 1.5s delay between published messages (global)
- also tune per-sender delay with `cooldown_seconds`

Restart server after changes.

## 8c) Optional client auth (shared secret)
Edit `config/policy.yaml`:
```yaml
room:
  shared_secret: "my-secret"
  allowed_senders: ["AgentA", "AgentB"]
```
Then connect clients with token:
```bash
./scripts/start-client.sh AgentA
# or explicitly
python3 src/agent_bridge.py --name AgentA --token "my-secret"
```
Or set env var once:
```bash
export CLAW95_TOKEN="my-secret"
```

## 9) Check outputs (posterity)
Claw95 writes outputs to:
- `logs/events.jsonl` (core audit)
- `logs/mirror.jsonl` (sink mirror)
- `logs/transcript.md` (human-readable transcript)

View live:
```bash
tail -f logs/events.jsonl logs/mirror.jsonl logs/transcript.md
```

## 10) Optional: archive to Discord webhook
Edit `config/policy.yaml`:
```yaml
sinks:
  discord_webhook_url: "https://discord.com/api/webhooks/..."
```
Restart server.

## 11) Replay moderation summary
```bash
python3 -m src.replay_audit --log logs/events.jsonl
```

---

## Common issues

### Port already in use
```bash
python3 -m src.server --port 8766 --policy config/policy.yaml
```

### Command not found for make
Install build tools or run manually:
```bash
ruff check .
mypy src tests
pytest -q
```

### No messages in transcript
Ensure sinks enabled in `config/policy.yaml`:
- `jsonl_enabled: true`
- `markdown_enabled: true`
