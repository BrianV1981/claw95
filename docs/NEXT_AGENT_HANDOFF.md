# Claw95 — Next Agent Handoff

## Project Status
Claw95 is being rebuilt around the new **POC / MVP PRD** in `docs/POC_MVP_PRD.md`.

The repo is now slightly beyond scaffold stage, but still firmly in early POC implementation.

## Current Source of Truth
1. `docs/POC_MVP_PRD.md` — active proof-of-concept target
2. `docs/WORKFLOW.md` — active development protocol, including GitOps Bridge adaptation
3. `docs/NEXT_AGENT_HANDOFF.md` — live continuation handoff
4. `docs/API.md` — current POC wire contract
5. code in `src/`

Older docs like `docs/ARCHITECTURE.md` and `docs/MODERATOR_SPEC.md` are still useful references, but they may not perfectly match the evolving POC implementation and should be aligned intentionally rather than assumed current.

## Completed This Session
### Documentation
- Added `docs/POC_MVP_PRD.md`
- Added `docs/WORKFLOW.md` to formalize TDD + GitOps Bridge-style issue-driven workflow
- Added this live handoff doc
- Rewrote `docs/API.md` to match the current POC implementation instead of the older aspirational payloads
- Updated `README.md` and `CONTRIBUTING.md` to point at the new workflow and POC-first direction

### TDD foundation
- Switched test execution to built-in `unittest` so the repo can be tested without installing pytest first
- Expanded moderator coverage from 2 tiny tests to a broader baseline covering:
  - malformed messages
  - policy matches
  - cooldown
  - rate limit
  - duplicates
  - rewrite behavior

### Implemented POC room controls
The server now supports these tested commands:
- `/pause`
- `/resume`
- `/topic <text>`

And now maintains room state fields for:
- `paused`
- `topic`
- `users`

### Added server tests
New tests verify:
- pausing updates room state
- resuming clears pause state
- topic updates room state
- paused rooms block normal message publication with `PAUSED`

## Current Code Snapshot
### `src/server.py`
Now includes:
- `handle_event(...)` entrypoint for unit-testable event handling
- command parsing
- room pause state
- room topic state
- command result events
- `room.state` broadcast including `paused` and `topic`
- graceful fallback when `websockets` is not installed, allowing unit tests to run

### `src/moderator.py`
Still simple, but now better covered by tests.

### `tests/test_moderator.py`
Uses `unittest` and is now a real baseline suite.

### `tests/test_server.py`
Covers current room control behavior.

## Current Test Command
Run:
```bash
python3 -m unittest discover -s tests -v
```

Current status: **green** (`11` tests passing at last run)

## What Is Still Missing vs POC
Major missing pieces relative to `docs/POC_MVP_PRD.md`:
- `/summary` command
- visible role-aware agent participation layer beyond simple target state
- richer auditability fields (`event_id`, clearer room metadata, policy version, etc.)
- better separation between human commands and agent discussion behavior
- cleanup/alignment pass on older architecture and moderator docs

## Recommended Next Slice
Next implementation slice should probably be:
1. add `/summary` with tests
2. add `/who` / `/help` or other minimum usability commands
3. start a minimal participant/role dispatch layer so targeted messages can influence room behavior rather than only tagging outbound messages

That moves the system from command/state correctness toward actual board-room interaction behavior.

## Documentation Rule
Do **not** leave scratch notes or hidden mental state.
If direction changes, update:
- `docs/NEXT_AGENT_HANDOFF.md`
- directly affected contract docs
- remove or rewrite contradicted documentation quickly

Prefer one current handoff doc over many temporary notes.
.
ntradicted documentation quickly

Prefer one current handoff doc over many temporary notes.
