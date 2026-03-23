# Claw95 — Next Agent Handoff

## Project Status
Claw95 is in early POC implementation and follows the updated GitOps Bridge doctrine:
- one long-lived phase branch per milestone
- atomic semantic pushes for every isolated slice
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
Active phase branch: `dev-phase-1`

Issues currently opened for phase work:
- `#5` — `/who` and `/help` room usability commands (implemented)
- `#4` — MIT license + OSS intake policy (implemented)
- `#6` — audit log event metadata hardening (implemented)
- `#7` — role-aware dispatch prompt event for targeted messages (implemented)
- `#8` — agent bridge reaction to role prompts (implemented)
- `#9` — replay/inspect utility for JSONL logs (implemented)
- `#10` — trace filtering metadata (`room_id`, `sender_type`, `command_category`) (implemented)
- `#11` — demo runbook for end-to-end proof flow (implemented)
- `#12` — runbook validation bug: direct `src/server.py` invocation fails; module-style invocation required (validated and documented)

## Completed POC Capabilities
Tested commands currently implemented:
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`
- `/who`
- `/help`

Room state currently includes:
- `paused`
- `topic`
- `users`
- `roles`
- `active_target`
- recent in-memory message history used by summaries

Targeted-message behavior now includes:
- `message.published` with `target`
- `room.role_prompt` emission when a message is sent with an active target role
- basic agent-bridge reply generation when an agent receives a matching role prompt

Audit logging now includes:
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

Demo runbook:
- `docs/DEMO_RUNBOOK.md` walks through server start, role bridge start, targeting, role prompt emission, agent reply, and log replay

## Test Status
Run:
```bash
python3 -m unittest discover -s tests -v
```

Status at last known green run: **28 tests passing**

## Known External Bug (Reported During Workflow)
`gitops promote` currently fails in upstream tool due to command runner argument conflict:
- error: `stdout and stderr arguments may not be used with capture_output`

Claw95 used manual equivalent promotion steps when needed.

## Current Missing Pieces vs POC
- richer agent behavior beyond deterministic templated replies
- alignment pass for older architecture/spec docs
- optional real browser/UI or terminal UX polish for demo friendliness

## Recommended Next Slice
1. do final doc-alignment sweep across legacy architecture/spec docs
2. optionally add richer role-specific response templates or pluggable role behavior
3. optionally validate the demo runbook live against the current runtime environment

## Documentation Rule
No scratch-note sprawl.
If behavior or workflow changes, update docs in the same slice.
Prune stale or conflicting content immediately.
y.
