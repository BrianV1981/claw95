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
4. `docs/NEXT_AGENT_HANDOFF.md` — live continuation handoff
5. `docs/API.md` — current POC wire contract
6. `docs/OSS_INTAKE.md` — OSS licensing/extraction policy
7. code in `src/`

## Branch / Git State
Active phase branch: `dev-phase-1`

Issues currently opened for phase work:
- `#5` — `/who` and `/help` room usability commands (implemented)
- `#4` — MIT license + OSS intake policy (implemented)
- `#6` — audit log event metadata hardening (implemented)
- `#7` — role-aware dispatch prompt event for targeted messages (implemented)

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

Audit logging now includes:
- `event_id` (UUID)
- `policy_version` (`poc-v1`)
- `ts`
- `event_type`
- event payload fields

## Test Status
Run:
```bash
python3 -m unittest discover -s tests -v
```

Status at last known green run: **21 tests passing**

Coverage includes:
- moderator decisions (malformed/policy/cooldown/rate/duplicate/rewrite)
- room pause/resume/topic controls
- ask-target selection + unknown agent rejection
- target propagation on published messages
- role prompt emission for targeted messages
- summary snapshot behavior including paused-room summary
- participant listing and help command behavior
- audit log metadata presence (`event_id`, `policy_version`)

## Known External Bug (Reported During Workflow)
`gitops promote` currently fails in upstream tool due to command runner argument conflict:
- error: `stdout and stderr arguments may not be used with capture_output`

Claw95 used manual equivalent promotion steps when needed.

## Current Missing Pieces vs POC
- actual agent execution/response flow tied to `room.role_prompt`
- richer auditability fields beyond baseline metadata (e.g., room IDs, replay helpers)
- alignment pass for older architecture/spec docs
- repo extraction matrix still recommended if external-repo mining becomes systematic

## Recommended Next Slice
1. add a small replay/inspect utility for JSONL events
2. improve log schema for trace filtering (`room_id`, sender type, command category)
3. start minimal agent-bridge reaction behavior for `room.role_prompt`

## Documentation Rule
No scratch-note sprawl.
If behavior or workflow changes, update docs in the same slice.
Prune stale or conflicting content immediately.
