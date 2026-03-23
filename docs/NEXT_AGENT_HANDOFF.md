# Claw95 — Next Agent Handoff

## Project Status
Claw95 is being rebuilt around the new **POC / MVP PRD** in `docs/POC_MVP_PRD.md`.

The repo is in early POC implementation with active GitOps-Bridge-native workflow.

## Current Source of Truth
1. `docs/POC_MVP_PRD.md` — active proof-of-concept target
2. `docs/WORKFLOW.md` — active development protocol (GitOps Bridge adapted)
3. `docs/NEXT_AGENT_HANDOFF.md` — live continuation handoff
4. `docs/API.md` — current POC wire contract
5. code in `src/`

## Workflow State
Current active issue branch: `fix/issue-3` (for `/summary`)

GitOps execution pattern now in use:
- `gitops bug`
- `gitops fix`
- TDD implementation slices
- `gitops push`

## Completed in recent slices
### Documentation
- Added `docs/POC_MVP_PRD.md`
- Added `docs/WORKFLOW.md`
- Reframed `README.md` as a true repo homepage
- Updated `CONTRIBUTING.md` to point at workflow + POC docs
- Updated `docs/API.md` for current command/state behavior

### Tested command/state behavior
Server now supports tested commands:
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`

Room state now includes:
- `paused`
- `topic`
- `users`
- `roles`
- `active_target`

Also includes in-memory recent message history used by `/summary`.

## Test Coverage Status
Run:
```bash
python3 -m unittest discover -s tests -v
```

Status at last run: **green** (`16` tests)

Coverage includes:
- moderator decisions (malformed/policy/cooldown/rate/duplicate/rewrite)
- room pause/resume/topic controls
- ask-target selection + unknown agent rejection
- target propagation on published messages
- summary snapshot behavior (including paused-room summary)

## Current Missing Pieces vs POC
- `/who` and `/help` commands
- role-aware dispatch behavior beyond message target tagging
- richer auditability fields (`event_id`, policy version, clearer structured metadata)
- alignment pass for older architecture/spec docs

## Recommended Next Slice
1. add `/who` and `/help` with tests
2. begin minimal role dispatch behavior tied to `active_target`
3. improve log schema for stronger audit/replay readiness

## Documentation Rule
No scratch-note sprawl.
If behavior/protocol changes, update docs in the same slice.
Prune stale or conflicting doc content immediately.
