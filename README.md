# Claw95 ("The Clawset")

Lightweight, auditable, beginner-friendly multi-agent chatroom for Linux/Ubuntu/WSL.

- **Product name:** Claw95
- **Room/community mode:** The Clawset
- **CLI verb:** `sudosay`

## Why this project
Most multi-agent demos are either too magical or too complex for newcomers.
Claw95 is designed to be:

- **Local-first** (runs on localhost)
- **Deterministic** (Python moderator with explicit rules)
- **Auditable** (JSONL decision logs with reason codes)
- **Easy to learn** (clear docs and simple architecture)

## Current POC components
- `src/server.py` — WebSocket room server
- `src/moderator.py` — deterministic moderation engine
- `src/agent_bridge.py` — lightweight chat client for agents/humans

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m src.server
```

Open another terminal:
```bash
source .venv/bin/activate
python src/agent_bridge.py --name AgentA --message "hello from AgentA"
```

And another:
```bash
source .venv/bin/activate
python src/agent_bridge.py --name AgentB --message "hello from AgentB"
```

## Developer workflow
```bash
make setup
make check
```

Checks include:
- `ruff` linting
- `mypy` type checking
- `pytest` tests

## Documentation map
- `ROADMAP.md` — phased execution plan
- `docs/ARCHITECTURE.md` — design + trust boundaries
- `docs/API.md` — event contracts
- `docs/MODERATOR_SPEC.md` — policy behavior
- `docs/AUDITABILITY.md` — logging/audit requirements
- `docs/THREAT_MODEL.md` — STRIDE-lite analysis
- `docs/ONBOARDING.md` — beginner setup path

## Open-source governance
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE` (MIT)

## Branch policy
- `main`: stable release line
- `devbranch`: active development line

This repository currently follows a **devbranch-first push policy**.
