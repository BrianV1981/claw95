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
6. code in `src/`

## Branch / Git State
Active phase branch: `dev-phase-1`

Issues currently opened for phase work:
- `#5` — `/who` and `/help` room usability commands
- `#4` — MIT license + OSS intake policy

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

## Test Status
Run:
```bash
python3 -m unittest discover -s tests -v
```

Status at last known green run: **18 tests passing**

Coverage includes:
- moderator decisions (malformed/policy/cooldown/rate/duplicate/rewrite)
- room pause/resume/topic controls
- ask-target selection + unknown agent rejection
- target propagation on published messages
- summary snapshot behavior including paused-room summary
- participant listing and help command behavior

## Current Missing Pieces vs POC
- role-aware dispatch behavior beyond message target tagging
- richer auditability fields (`event_id`, policy version, clearer metadata)
- MIT license + OSS intake policy still pending
- alignment pass for older architecture/spec docs

## Recommended Next Slice
1. add MIT license and third-party intake policy
2. begin minimal role dispatch behavior tied to `active_target`
3. improve log schema for audit/replay readiness

## Documentation Rule
No scratch-note sprawl.
If behavior or workflow changes, update docs in the same slice.
Prune stale or conflicting content immediately.
