# OpenClaw Subagent Bridge (Local, No Discord)

This bridge lets Claw95 route room prompts to OpenClaw subagents and post replies back.

## Current mapping
Configured in `config/subagent_bridge.yaml`:
- `@ops` -> OpenClaw agent `ops`
- `@qa` -> OpenClaw agent `reviewer`

## Start sequence
1. Start room server:
```bash
./scripts/start-safe.sh
```
2. In a new terminal, start bridge:
```bash
cd ~/claw95
./scripts/start-subagent-bridge.sh
```
3. In another terminal, join as a user/client:
```bash
cd ~/claw95
./scripts/start-client.sh User
```

## Usage
In client chat, mention target agent:
- `@ops give me a deployment checklist`
- `@qa review this plan for test gaps`

Bridge will call OpenClaw and post responses back into room as:
- `[ops] ...`
- `[qa] ...`

## Config
`config/subagent_bridge.yaml`
- `trigger_mode`: `mention` or `all`
- `max_concurrent`: in-flight subagent calls
- `request_timeout_seconds`
- `session_mode`: `room` (stable per-agent room memory) or `stateless` (new session per request)
- `response_max_chars`: cap long replies
- `agent_map`

## Notes
- Local-first: no Discord required.
- Keep mention mode on to avoid accidental loops.
- If OpenClaw CLI command surface differs, adapt command in `src/openclaw_subagent_bridge.py`.
