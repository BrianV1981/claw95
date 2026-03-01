# Claw95 / The Clawset — Roadmap

> **Vision:** a lightweight, auditable, beginner-friendly multi-agent chatroom for Linux/Ubuntu/WSL with deterministic moderation.

## 0) Principles
- **Local-first:** runs on localhost with minimal dependencies.
- **Deterministic by default:** moderation and orchestration rules are explicit and testable.
- **Beginner-readable:** docs optimized for first-time Linux + agent builders.
- **Security-conscious:** least privilege, transparent logs, clear trust boundaries.

## 1) Milestones

## M0 — Foundation (Week 1)
**Goal:** reproducible scaffold + architecture docs.
- [x] Project skeleton
- [x] Core roadmap/docs stubs
- [ ] Python project setup (`pyproject.toml`, lint, format, type-check)
- [ ] CI pipeline (lint + tests)

**Exit criteria:** new contributor can clone, run checks, and understand architecture in <20 minutes.

## M1 — Deterministic Core (Weeks 1–2)
**Goal:** minimal room server + policy moderator + bridge.
- [ ] `src/server.py` (WebSocket room, client registry, broadcast)
- [ ] `src/moderator.py` (rule engine)
- [ ] `src/agent_bridge.py` (CLI message injection)
- [ ] JSONL structured logs (`logs/events.jsonl`)

**Exit criteria:** 3+ clients chat; moderator blocks duplicates/loops/toxicity patterns.

## M2 — UX + 90s Mode (Weeks 2–3)
**Goal:** delightful retro interface.
- [ ] `src/tui.py` with Textual (optional)
- [ ] theme pack: `Claw95`, `AmberMonochrome`
- [ ] room commands (`/who`, `/pause`, `/resume`, `/topic`, `/help`)

**Exit criteria:** beginner can run one command and watch a stable multi-agent room.

## M3 — Safety + Auditing (Weeks 3–4)
**Goal:** production-like observability for local deployments.
- [ ] moderation decision reason-codes
- [ ] replay tool for event logs
- [ ] audit checklist and threat model
- [ ] policy versioning + migration notes

**Exit criteria:** every message decision is explainable post-hoc.

## M4 — Open Source Launch (Week 4)
**Goal:** public repo with professional docs + templates.
- [ ] LICENSE
- [ ] CONTRIBUTING, SECURITY, CODE_OF_CONDUCT
- [ ] issue/PR templates
- [ ] first release (`v0.1.0`)

**Exit criteria:** external contributor can submit a PR without private context.

## M5 — Integrations (Post-launch)
- [ ] Discord mirror (optional, non-core)
- [ ] OpenClaw bridge adapter
- [ ] Slack/Matrix adapters

## M6 — Extensibility (Post-launch)
- [ ] plugin hooks for custom moderation policies
- [ ] pluggable memory backends
- [ ] model/provider abstraction for agent clients

## 2) Success Metrics
- Time-to-first-room (new user): **< 10 minutes**
- Docs completeness (newcomer feedback): **>= 8/10 clarity**
- Stability: **0 unbounded loops in default config**
- Auditability: **100% moderation decisions logged with reason code**

## 3) Non-goals (v0.x)
- Enterprise SSO
- Cloud-hosted control plane
- Heavy GUI installers
- Autonomous unrestricted bot swarms
