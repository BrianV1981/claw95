# Claw95 / The Clawset — Roadmap

> **Vision:** a local-first, auditable, beginner-readable real-time AI board room with deterministic moderation.

## 0) Principles
- **Local-first:** runs on localhost with minimal dependencies.
- **Deterministic by default:** moderation and orchestration rules are explicit and testable.
- **Beginner-readable:** docs should help a newcomer understand the system quickly.
- **Proof-first:** prove the board-room loop before overbuilding infrastructure.

## 1) Current Milestones

## M0 — Foundation and Repo Clarity
**Goal:** establish product direction, workflow discipline, and onboarding clarity.
- [x] Project skeleton
- [x] README rewritten as repo homepage
- [x] POC PRD added
- [x] workflow docs added
- [x] live handoff doc added
- [x] MIT license added
- [x] OSS intake policy added
- [ ] Python project setup (`pyproject.toml`, lint, format, type-check)
- [ ] CI pipeline (lint + tests)

## M1 — Deterministic Core Room
**Goal:** minimal room server + moderator + bridge + test coverage.
- [x] `src/server.py`
- [x] `src/moderator.py`
- [x] `src/agent_bridge.py`
- [x] JSONL structured logging
- [x] replay/inspect utility (`src/replay.py`)
- [x] unittest-based test suite

## M2 — Board-Room Interaction Loop
**Goal:** prove visible targeted collaboration in-room.
- [x] room commands: `/pause`, `/resume`, `/topic`, `/ask`, `/summary`, `/who`, `/help`
- [x] role-aware target state
- [x] `room.role_prompt` events
- [x] basic agent-bridge reaction to matching role prompts
- [x] demo runbook for end-to-end proof flow

## M3 — Auditability / Traceability
**Goal:** make room behavior inspectable enough for the POC.
- [x] moderation reason codes
- [x] `event_id`
- [x] `policy_version`
- [x] `room_id`
- [x] trace fields such as `sender_type` and `command_category`
- [x] replayable JSONL logs
- [ ] richer replay helpers / filtering UX

## M4 — POC Polish
**Goal:** tighten the repo so a newcomer can run and understand the demo quickly.
- [ ] validate demo runbook live against runtime
- [ ] align any remaining legacy docs to implemented behavior
- [ ] optional richer deterministic role templates
- [ ] optional simple TUI / presentation polish

## M5 — Future / Post-POC
- [ ] richer agent reasoning and orchestration
- [ ] integrations (Discord/OpenClaw/Slack/Matrix)
- [ ] pluggable role behaviors
- [ ] memory/provider abstractions
- [ ] public release / packaging improvements

## 2) Success Metrics
- newcomer can understand the repo quickly from README + POC docs
- room commands behave deterministically under test
- targeted board-room flow is demonstrable end-to-end
- logs are explainable and inspectable

## 3) Non-goals (Current POC)
- enterprise SSO
- cloud-hosted control plane
- unrestricted autonomous bot swarms
- large plugin platform before the core loop is proven
