# Clawset (working title)

A lightweight multi-agent chatroom for Linux/Ubuntu/WSL with a deterministic Python moderator.

## Goals
- 90s-style chatroom vibe
- Multiple AI agents in one room
- Simple local-first architecture
- Strong guardrails via Python moderator script

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
