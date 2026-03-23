# Clawset (working title)

A local-first **real-time AI board room** for Linux/Ubuntu/WSL where multiple specialized agents collaborate in one visible room while a human can interject at any time.

Claw95 uses a deterministic Python moderator to keep the room readable, auditable, and resistant to spam or loop behavior.

## Current Direction
The project is currently being built as a **proof of concept first**.

Primary source-of-truth docs:
- `docs/POC_MVP_PRD.md`
- `docs/WORKFLOW.md`
- `docs/NEXT_AGENT_HANDOFF.md`

## Goals
- 90s-style chatroom vibe
- Multiple specialized AI agents in one room
- Real-time visible collaboration
- Human participation in the same room
- Simple local-first architecture
- Strong guardrails via deterministic Python moderation

## Initial structure
- `src/` — app code (server, moderator, clients)
- `config/` — room and policy config (YAML/JSON)
- `logs/` — transcripts and moderation events
- `tests/` — unit/integration tests
- `docs/` — design notes and protocol docs

## Proposed first files
- `src/server.py`
- `src/moderator.py`
- `src/agent_bridge.py`
- `src/tui.py`
- `config/policy.yaml`

## Name ideas (shortlist)
- **Clawset** — funny, memorable, community-friendly
- **Claw95** — brand-aligned + instant retro signal
- **SudoSay** — command-line charm, very dev-native
- **BotNETscape** — nostalgic and clever, but less broad appeal

## Name strategy recommendation
- Product: **Claw95**
- Room mode: **The Clawset**
- CLI command: **sudosay**

This gives you a layered brand that is playful and practical.
