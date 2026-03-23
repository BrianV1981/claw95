# Claw95 — Next Agent Handoff

## Project Status
Claw95 has completed Phase 1 and is now on `dev-phase-2` for live AI-agent integration.

Working doctrine remains:
- one long-lived phase branch per milestone
- atomic semantic pushes for each isolated slice
- immediate documentation updates
- no note sprawl

## Current Source of Truth
1. `README.md` — repo homepage / product framing
2. `docs/POC_MVP_PRD.md` — active proof-of-concept target
3. `docs/WORKFLOW.md` — active development protocol
4. `docs/API.md` — current POC wire contract
5. `docs/DEMO_RUNBOOK.md` — end-to-end proof/demo runbook
6. `docs/NEXT_AGENT_HANDOFF.md` — live continuation handoff
7. `docs/OSS_INTAKE.md` — OSS licensing/extraction policy
8. code in `src/`

## Branch / Git State
Active phase branch: `dev-phase-2`

Relevant issues:
- `#13` — add real Ollama-backed agent participation and prove two-agent room communication (in progress; live proof already achieved)

## Proven Capabilities
### Core room behavior
Implemented and tested commands:
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`
- `/who`
- `/help`

Room state includes:
- `paused`
- `topic`
- `users`
- `roles`
- `active_target`
- recent in-memory message history used by summaries

### Targeted role behavior
Targeted-message flow now includes:
- `message.published` with `target`
- `room.role_prompt` emission when a message is sent with an active target role
- self-loop prevention so a role does not re-prompt itself on its own reply
- agent-bridge reply generation for matching role prompts
- optional first-class handoff from one role to another via `handoff.submit`
- server-emitted `room.handoff` + target `room.role_prompt` on handoff

### Agent provider behavior
`src/agent_bridge.py` now supports:
- `deterministic` provider mode
- `ollama` provider mode
- configurable `--model`
- optional `--next-role`
- `--handoff-delay-seconds` to avoid cooldown collisions on immediate handoff

### Live validation already achieved
Validated live with local Ollama:
- `strategist` on `ollama` (`llama3.2:latest`)
- `critic` on `ollama` (`llama3.2:latest`)
- human prompt targeted to `strategist`
- strategist generated a real local-model reply
- strategist handed off to critic
- critic generated a real local-model reply

This means Claw95 has now proven:
- human → AI role prompt
- AI role → second AI role handoff
- local LLM-backed in-room communication

## Audit / Replay Status
Audit logging includes:
- `event_id` (UUID)
- `policy_version` (`poc-v1`)
- `room_id` (`main`)
- `sender_type` where applicable
- `command_category` for room commands
- `ts`
- `event_type`
- event payload fields

Replay utility:
- `src/replay.py` supports loading/filtering JSONL events and printing readable summaries

## Test Status
Run:
```bash
python3 -m unittest discover -s tests -v
```

Status at last green run: **32 tests passing**

## Known Runtime Notes
- module-style invocation remains required:
  - `python3 -m src.server`
  - `python3 -m src.agent_bridge`
  - `python3 -m src.replay`
- current runtime still emits `websockets.* is deprecated` warnings; functional, but worth cleaning up in a future slice
- immediate handoff without delay can collide with moderation cooldown; use `--handoff-delay-seconds` when chaining roles

## Recommended Next Slice
1. commit the Ollama integration + self-loop guard + docs update
2. decide whether role handoff should stay command-driven or become a first-class server event
3. optionally add role-specific prompt templates / context windows per role
4. optionally add a third Ollama-backed role (`researcher` or `synthesizer`)
5. optionally remove websocket deprecation warnings by updating imports/API usage

## Documentation Rule
No scratch-note sprawl.
If behavior or workflow changes, update docs in the same slice.
Prune stale or conflicting content immediately.
