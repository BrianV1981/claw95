# Claw95 Development Workflow

## Purpose
This document defines the active development workflow for Claw95.

It incorporates the useful operating protocol from `gitops-bridge` and adapts it to Claw95's current proof-of-concept stage.

The goal is to keep development:
- issue-driven
- test-driven
- well documented
- easy for the next agent or contributor to continue
- free of scattered mental notes and stale scratch docs

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
- `docs/POC_MVP_PRD.md`
- `docs/NEXT_AGENT_HANDOFF.md`
- `docs/API.md`
- this file, when workflow changes

### 3. No note sprawl
Do not leave disconnected temporary notes, random scratch docs, or stale contradictory files lying around.

If a doc becomes outdated:
- update it
- prune it
- or explicitly mark it as historical / non-authoritative

### 4. Small slices over giant rewrites
Prefer small, testable, documented increments.

---

## GitOps Bridge Protocol (Adapted)
Claw95 adopts the useful parts of the `gitops-bridge` philosophy:
- issue-driven development
- isolated branch-per-problem work
- semantic commit intent
- atomic releases / changesets
- automated version + changelog flow when available

### The Operating Model
1. **Report the issue or task**
2. **Isolate work on a dedicated branch**
3. **Implement in small TDD slices**
4. **Push with semantic intent**
5. **Promote only after verification**

---

## Recommended 4-Step Workflow
### Step 1 — Report / track the work
If GitHub issues are in use and `gitops` is available:
```bash
gitops bug "Room pause command does not prevent message publication"
```

If issues are not being created formally yet, record the active work clearly in:
- `docs/NEXT_AGENT_HANDOFF.md`
- or the active issue tracker

### Step 2 — Isolate the work
If `gitops` is available:
```bash
gitops fix <issue-id>
```
This creates a focused issue branch like:
```bash
fix/issue-4
```

If `gitops` is not available, use the same branch naming style manually.

### Step 3 — Implement with TDD and semantic intent
Work in small slices.
Every slice should aim to keep:
- tests green
- docs current
- behavior understandable

When ready to commit and push, prefer GitOps Bridge if installed:
```bash
gitops push "Fix: Added room pause state enforcement (Closes #4)"
```

### Step 4 — Promote after verification
When a branch is validated and ready to merge:
```bash
gitops promote
```

This preserves the GitOps Bridge archive/promote philosophy and avoids ad hoc branch chaos.

---

## Atomic Change Rule
Claw95 adopts the **atomic deployment rule** from `gitops-bridge`:

> Do not batch unrelated changes into one mega-commit when they should be separate logical slices.

For Claw95 this means:
- one bug fix = one logical change slice
- one protocol addition = one logical change slice
- one behavior change = tests + code + docs together

The purpose is to preserve:
- clean history
- understandable changelog entries
- easier rollback
- easier handoff to the next agent

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
- `Fix:` for bug fixes or broken behavior
- `Feature:` for meaningful new POC capability
- `Docs:` for documentation-only work
- `Chore:` for cleanup, maintenance, or non-product adjustments

---

## When GitOps Bridge Is Available
If `gitops` is installed and working in the repository environment:
- prefer `gitops bug`
- prefer `gitops fix`
- prefer `gitops push`
- prefer `gitops promote`

And avoid raw manual:
- `git commit`
- `git push`
- hand-editing `CHANGELOG.md`
- hand-editing `VERSION`

---

## When GitOps Bridge Is Not Available
Claw95 should still follow the protocol conceptually.

Fallback behavior:
- create or reference an issue/task explicitly
- use isolated issue-style branches
- use semantic commit messages manually
- keep changes atomic
- update docs in the same pass
- preserve clear handoff state in `docs/NEXT_AGENT_HANDOFF.md`

The workflow matters more than the tool itself.

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

Do not optimize for release ceremony before the POC is proven.
But do preserve enough workflow discipline that the project can scale cleanly once proven.
