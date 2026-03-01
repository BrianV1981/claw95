# Claw95 ("The Clawset")

A lightweight, auditable, beginner-friendly multi-agent chatroom for Linux/Ubuntu/WSL.

> **Status:** v0.1.0-rc1 (open preview)

- **Product name:** Claw95
- **Room mode:** The Clawset
- **CLI verb:** `sudosay` (planned helper command)

## Why this exists
Most multi-agent demos are either too magical or too complex for newcomers.
Claw95 is built to be understandable first, then extensible.

## Core features
- Local WebSocket room server
- Deterministic Python moderator with reason codes
- Configurable policy (`config/policy.yaml`)
- Interactive bridge client for agents/humans
- Room commands: `/help`, `/who`, `/pause`, `/resume`, `/topic`, `/stats`
- JSONL audit logs + replay summary tool

## Quickstart (under 10 minutes)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
python -m src.server --policy config/policy.yaml
```

Open terminal 2:
```bash
source .venv/bin/activate
python src/agent_bridge.py --name AgentA
```

Open terminal 3:
```bash
source .venv/bin/activate
python src/agent_bridge.py --name AgentB
```

Now type messages or commands in either bridge terminal:
- `/help`
- `/topic Building the future of agent chat`
- `/stats`

## Audit replay
After chatting, summarize events:
```bash
python -m src.replay_audit --log logs/events.jsonl
```

## Developer workflow
```bash
make setup
make check
```

Checks include Ruff, mypy, and pytest (unit + integration).

## Documentation map
- `ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/MODERATOR_SPEC.md`
- `docs/REASON_CODES.md`
- `docs/AUDITABILITY.md`
- `docs/THREAT_MODEL.md`
- `docs/DEEP_REVIEW.md`
- `docs/RELEASE.md`
- `docs/MERGE_CHECKLIST.md`

## Open-source governance
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CODE_OF_CONDUCT.md`
- `LICENSE` (MIT)

## Branch policy
- `main`: stable line
- `devbranch`: active development line

This repository currently follows a **devbranch-first push policy**.
