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

## Restart workflow
1. Stop server (`Ctrl+C` in server terminal).
2. Restart:
   ```bash
   ./scripts/start-dev.sh
   ```

## Fast local demo mode
Run everything at once:
```bash
./scripts/start-room.sh
```
This starts server + AgentA + AgentB and stops all on Ctrl+C.

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
