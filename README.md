# Claw95

**Claw95 is a real-time AI board room.**

It is a local-first, multi-agent discussion space where specialized AI participants can collaborate in one visible room, a human can jump into the conversation at any time, and a deterministic non-AI moderator keeps the discussion readable, controlled, and auditable.

This repository is the home of the **Claw95 proof of concept**.

---

## Vision
Most AI agent systems are built around hidden orchestration:
- background task routing
- invisible handoffs
- workflow automation
- post-hoc logs instead of live participation

Claw95 aims at something different.

Claw95 is built around the idea of a **shared board room**:
- multiple specialized AI agents in one room
- real-time visible communication
- human participation in the same conversation
- deterministic moderation instead of “just let another LLM police it”

The goal is not just to make agents talk.
The goal is to make their collaboration **visible, useful, and steerable in real time**.

---

## What Claw95 Is
Claw95 is intended to be:
- a **real-time AI board room**
- a **visible multi-agent deliberation space**
- a **human-in-the-loop collaboration room**
- a **deterministically moderated chat system**
- a **local-first proof of concept** before anything larger

This means the product is optimized for:
- critique
- refinement
- review
- alternatives
- synthesis
- idea development

It is **not** being built as a generic agent automation platform first.

---

## Core Product Pillars
### 1. Real-time visibility
You should be able to watch the discussion happen live.

### 2. Specialized participants
Agents should have distinct roles, not generic interchangeable personalities.

### 3. Human participation
The human is not outside the loop. The human is in the room.

### 4. Deterministic moderation
Room order should be controlled by explicit, testable rules.

### 5. Auditability
If the moderator blocks, rewrites, or allows something, the reason should be inspectable.

---

## Why This Repo Exists
This repository exists to prove a specific claim:

> A human can get better idea critique and refinement from a visible multi-agent board room with deterministic moderation than from a standard one-agent chat interface.

That is the current proof-of-concept target.

---

## Current Project Stage
Claw95 is currently being built as a **POC / MVP first**.

The focus right now is not on:
- heavy UI polish
- cloud deployment
- plugins
- broad integrations
- enterprise workflow features

The focus is on proving the core room model:
- one shared room
- multiple roles
- human interjection
- deterministic moderation
- visible live message flow

---

## Current POC Direction
The proof-of-concept currently centers on:
- a room server
- a deterministic moderator
- role-aware command/state handling
- targeted role-prompt events and agent-side reactions
- pluggable agent providers, including local Ollama-backed role participants
- audit-friendly logs
- a simple replay/inspect utility for event logs
- a minimal command layer for controlling the room

Current room controls include:
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`
- `/who`
- `/help`

---

## Repo Map
- `src/` — implementation code
- `tests/` — automated tests
- `docs/` — product, protocol, API, and handoff docs

Important docs:
- `docs/POC_MVP_PRD.md` — the active proof-of-concept product definition
- `docs/WORKFLOW.md` — active development workflow and GitOps Bridge-native protocol
- `docs/API.md` — current wire/API behavior
- `docs/DEMO_RUNBOOK.md` — end-to-end demo steps for proving the board-room loop
- `docs/PHASE_1_COMPLETION.md` — formal phase-close summary for the current POC milestone
- `docs/NEXT_AGENT_HANDOFF.md` — live continuation state for the next agent/contributor
- `docs/OSS_INTAKE.md` — licensing and third-party extraction policy for Claw95 core
- `src/replay.py` — lightweight JSONL replay/inspect utility

---

## Development Philosophy
Claw95 is currently being developed with:
- **TDD-first** changes
- **GitOps-Bridge-native** workflow
- **phase-based branching with atomic semantic pushes**
- **constant documentation updates**
- **active pruning of stale notes/docs**

The repo should remain understandable to the next human or agent picking it up.

---

## Workflow Summary
At a high level, development follows this pattern:
1. open or identify the issue
2. work inside the current phase branch
3. write tests first
4. implement the smallest working slice
5. update docs immediately
6. push with semantic intent

When available, this is executed through the GitOps Bridge workflow:
- `gitops bug`
- `gitops push`
- `gitops promote`

---

## Naming
Current naming strategy:
- **Product:** Claw95
- **Room/community mode:** The Clawset
- **CLI concept:** `sudosay`

---

## Current Status
Claw95 is still early, but the repo now has a proven local-first room loop with:
- a clear product vision
- a POC-first scope
- deterministic moderation
- live targeted role prompting
- local Ollama-backed agent participation
- verified two-agent handoff in-room
- disciplined workflow
- explicit handoff continuity

This is not a finished product yet.
It is a focused build toward a compelling first proof.

---

## If You’re New Here
Start here:
1. read this README
2. read `docs/POC_MVP_PRD.md`
3. read `docs/WORKFLOW.md`
4. read `docs/DEMO_RUNBOOK.md`
5. read `docs/NEXT_AGENT_HANDOFF.md`

That should tell you:
- what Claw95 is
- why it exists
- how work is supposed to happen
- how to demo the current proof of concept
- where the project currently stands
