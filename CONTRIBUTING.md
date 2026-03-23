# Contributing

Thanks for helping build Claw95.

## First Read
Before making meaningful changes, read:
1. `docs/POC_MVP_PRD.md`
2. `docs/WORKFLOW.md`
3. `docs/NEXT_AGENT_HANDOFF.md`

## Setup
1. Install Python 3.11+
2. Create venv
3. Install deps
4. Run tests

Current built-in test command:
```bash
python3 -m unittest discover -s tests -v
```

## Development Protocol
Claw95 currently follows:
- **TDD-first** changes
- **issue-driven / isolated branch** workflow
- immediate documentation updates
- no stale note sprawl

If `gitops` from GitOps Bridge is available in the environment, prefer:
- `gitops bug`
- `gitops fix <id>`
- `gitops push "Prefix: message"`
- `gitops promote`

If not available, follow the same protocol manually.

## Branch Strategy
Preferred pattern:
- `main` is stable
- `fix/issue-<id>` for bug work
- `feature/issue-<id>` or similarly scoped isolated branches for features

## Commit / Push Style
Preferred semantic intent:
- `Feature:` new feature
- `Fix:` bug fix
- `Docs:` documentation
- `Chore:` maintenance / cleanup
- `BREAKING CHANGE:` incompatible behavior change

## Pull Requests
A PR should include:
- problem statement
- design decision
- test coverage
- docs updates (if behavior changed)
- handoff impact if current workflow/state changed

## Definition of Done
- tests pass
- behavior is documented
- `docs/NEXT_AGENT_HANDOFF.md` updated when appropriate
- stale conflicting notes/docs are cleaned up
- audit impact reviewed when relevant
