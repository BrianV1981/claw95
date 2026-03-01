# Operations Guide

## Runtime commands (in client)
- `/help`
- `/who`
- `/topic <text>`
- `/stats`
- `/config`
- `/health`
- `/pause`
- `/resume`

## Log files
- `logs/events.jsonl` — canonical audit log
- `logs/mirror.jsonl` — sink mirror
- `logs/transcript.md` — readable transcript

## Live monitoring
```bash
tail -f logs/events.jsonl logs/mirror.jsonl logs/transcript.md
```

## Preflight
Before demos or review sessions:
```bash
./scripts/preflight.sh
```

## Doctor
For runtime + sink diagnostics:
```bash
./scripts/doctor.sh
```

## Restart workflow
1. Stop server (`Ctrl+C` in server terminal).
2. Restart:
   ```bash
   ./scripts/start-dev.sh
   ```

## Fast local demo mode
Preferred (interactive, one terminal via tmux):
```bash
./scripts/dev-stack.sh
tmux attach -t claw95
```
Includes 4 panes: server, subagent bridge, User client, log tail.

Alternative (requested): server on one tab + user/3 bots on second tab:
```bash
./scripts/dev-stack-2tab.sh
tmux attach -t claw95-2tab
```
Window 1 = server, Window 2 = User + OpsBot + QABot + GrowthBot.
Use `Ctrl+b` then `n` / `p` to switch tabs.

Stop:
```bash
./scripts/dev-stack-stop.sh
```

Watch-only mode:
```bash
./scripts/start-room.sh
```
This starts server + AgentA + AgentB watch clients and stops all on Ctrl+C.

Optional port override:
```bash
CLAW95_PORT=8766 ./scripts/start-room.sh
CLAW95_PORT=8766 ./scripts/dev-stack.sh
```

## Config change workflow
1. Edit `config/policy.yaml`.
2. Restart server.
3. Run `/config` from a client to confirm active values.

## Recommended defaults
- `cooldown_seconds: 2-5`
- `room.global_min_interval_ms: 1000-2500`
- `sinks.markdown_enabled: true`
- `sinks.jsonl_enabled: true`

## Safety notes
- Keep server bound to localhost unless intentionally exposing through a secured proxy.
- Enable `room.shared_secret` for client join auth if multiple local users/processes can connect.
- Optionally restrict identities with `room.allowed_senders` (allowlist of sender IDs).
- Do not store webhook secrets in public repos.
