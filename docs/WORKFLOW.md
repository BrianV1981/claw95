# Claw95 Development Workflow

## Purpose
This document defines the active development workflow for Claw95.

Claw95 follows a **GitOps-Bridge-native** process adapted to the current proof-of-concept stage.

The goal is to keep development:
- test-driven
- issue-aware
- deployment-oriented
- continuously documented
- free of branch spam and note sprawl

---

## Core Rules
### 1. TDD first
For any meaningful behavior change:
1. write or expand the failing test first
2. implement the smallest change that makes it pass
3. refactor only after green tests
4. update docs immediately if behavior or workflow changed

### 2. Documentation is part of the work
If code changes the product, protocol, or current state of the project, update the relevant docs **in the same work pass**.

At minimum, keep these current:
- `README.md`
- `docs/POC_MVP_PRD.md`
- `docs/API.md`
- `docs/NEXT_AGENT_HANDOFF.md`
- this file

### 3. No note sprawl
Do not leave disconnected temporary notes, random scratch docs, or stale contradictory files lying around.

If a doc becomes outdated:
- update it
- prune it
- or explicitly mark it as historical / non-authoritative

### 4. Small slices over giant rewrites
Prefer small, testable, documented increments.

---

## GitOps Bridge Protocol (Current Interpretation)
Claw95 adopts the updated GitOps Bridge doctrine:
- work is tracked with issues/tasks
- work is organized into **strategic phases / milestones**
- each phase uses **one long-lived branch**
- each isolated fix or feature inside that phase gets its own immediate **atomic semantic push**

### The Operating Model
1. **Track the issue or task**
2. **Work inside the current phase branch**
3. **Implement in small TDD slices**
4. **Deploy each slice immediately with `gitops push`**
5. **Promote the whole phase branch when the milestone is ready**

---

## Phase Protocol (Branching)
Do **not** create a new branch for every tiny change.

Preferred pattern:
- `main` = stable baseline
- `dev-phase-1` or similar = active milestone branch
- stay on that phase branch for the duration of the milestone

Issues still matter, but they do **not** require separate micro-branches.
They serve as work tracking and closure references for individual pushes.

---

## Atomic Deployment Rule (Pushing)
While staying on one phase branch for a longer period, deploy continuously to that branch.

> Every isolated bug fix, test addition, feature addition, doc correction, or cleanup slice should be pushed immediately with its own `gitops push` command.

Examples:
```bash
gitops push "Feature: added /who room command (Closes #4)"
gitops push "Fix: corrected summary payload target handling (Closes #5)"
gitops push "Docs: aligned API contract with current room state"
```

Do **not** batch unrelated changes into one mega-commit.

---

## Recommended Workflow
### Step 1 — Track the work
If GitHub issues are in use and `gitops` is available:
```bash
gitops bug "POC lacks /who command for participant visibility"
```

If the work is not a bug, still track it clearly through the issue system or a deliberate milestone plan.

### Step 2 — Stay on the active phase branch
Use one branch per phase, for example:
```bash
git checkout -b dev-phase-1
```

If the branch already exists, continue using it.
Do not branch-hop for every tiny slice.

### Step 3 — Implement with TDD
Every slice should aim to keep:
- tests green
- docs current
- behavior understandable

### Step 4 — Push every slice semantically
When a slice is complete, deploy it immediately:
```bash
gitops push "Feature: added /help command"
```

### Step 5 — Promote the phase branch
When the milestone is validated and ready for baseline:
```bash
gitops promote
```

---

## Semantic Commit / Release Intent
When using GitOps Bridge, commit messages should use semantic prefixes.

### Preferred prefixes
- `Feature:` — new capability
- `Fix:` — bug fix / correction
- `Docs:` — documentation-only change
- `Chore:` — maintenance / cleanup
- `BREAKING CHANGE:` — incompatible change

### Practical Claw95 guidance
Use:
- `Feature:` for meaningful POC capability additions
- `Fix:` for behavior corrections
- `Docs:` for documentation-only work
- `Chore:` for cleanup, workflow alignment, or non-product maintenance

---

## Absolute Mandates
When GitOps Bridge is available:
- prefer `gitops bug`
- prefer `gitops push`
- prefer `gitops promote`
- do not hand-edit `CHANGELOG.md`
- do not hand-edit `VERSION`
- avoid raw `git commit` / `git push` for normal development flow

Note: if GitOps Bridge helper commands lag behind the documented branching doctrine, follow the **documented doctrine** for branch strategy and still use `gitops push` / `gitops promote` for deployment steps.

---

## Required Handoff Discipline
At the end of any meaningful work session:
1. update `docs/NEXT_AGENT_HANDOFF.md`
2. record what changed
3. record what is currently green / verified
4. record the next recommended slice
5. remove or rewrite any stale note that would confuse the next agent

The next agent should not need tribal knowledge.

---

## Current Workflow Priority for Claw95
At this stage of the POC, this order matters most:
1. tests
2. code
3. docs
4. semantic history hygiene
5. branch cleanliness

Do not optimize for ceremony over progress.
Do preserve enough discipline that the repo can scale without chaos.
