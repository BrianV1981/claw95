# Claw95 — Next Agent Handoff

## Project Status
Claw95 is in early POC implementation and now follows the **updated GitOps Bridge doctrine**:
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
Short-lived issue branches were used earlier while the GitOps Bridge doctrine was still being interpreted.
That has now been superseded.

Current intent after cleanup:
- merge completed short-lived branches into `main`
- delete stale issue branches
- continue future work on a proper phase branch instead of per-issue micro-branches

## Completed POC Capabilities
Tested commands currently implemented:
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`

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

Status at last known green run: **16 tests passing**

Coverage includes:
- moderator decisions (malformed/policy/cooldown/rate/duplicate/rewrite)
- room pause/resume/topic controls
- ask-target selection + unknown agent rejection
- target propagation on published messages
- summary snapshot behavior including paused-room summary

## Current Missing Pieces vs POC
- `/who` and `/help` commands
- role-aware dispatch behavior beyond message target tagging
- richer auditability fields (`event_id`, policy version, clearer metadata)
- alignment pass for older architecture/spec docs
- MIT license + OSS intake policy still recommended

## Recommended Next Slice
On the next proper phase branch:
1. add `/who` and `/help` with tests
2. begin minimal role dispatch behavior tied to `active_target`
3. improve log schema for audit/replay readiness
4. add MIT license and third-party intake policy before deeper repo extraction work

## Documentation Rule
No scratch-note sprawl.
If behavior or workflow changes, update docs in the same slice.
Prune stale or conflicting content immediately.
