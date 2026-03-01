# Quick Start (Claw95 on devbranch)

This is the fastest path to get Claw95 running locally.

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

## 4) Start server (Terminal 1)
```bash
source .venv/bin/activate
python3 -m src.server --policy config/policy.yaml
```

Or one-command launcher:
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
