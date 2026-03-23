# Contributing

Thanks for helping build Claw95.

## First Read
Before making meaningful changes, read:
1. `README.md`
2. `docs/POC_MVP_PRD.md`
3. `docs/WORKFLOW.md`
4. `docs/NEXT_AGENT_HANDOFF.md`

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
- **phase-based branching**
- **atomic semantic pushes**
- immediate documentation updates
- no stale note sprawl

If `gitops` from GitOps Bridge is available in the environment, prefer:
- `gitops bug`
- `gitops push "Prefix: message"`
- `gitops promote`

## Branch Strategy
Preferred pattern:
- `main` is stable
- one active **phase branch** per milestone, for example `dev-phase-1`
- do not create a brand-new branch for every tiny bug or feature slice

Issues are still encouraged for tracking, but atomic slices should normally land on the current phase branch.

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
