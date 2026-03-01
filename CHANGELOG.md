# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [0.1.0] - 2026-03-01
### Added
- Initial proof-of-concept room server (`src/server.py`)
- Deterministic moderation engine (`src/moderator.py`)
- Agent bridge client (`src/agent_bridge.py`) with interactive mode
- Policy config loader (`src/policy.py`) and default `config/policy.yaml`
- Event schema validation (`src/events.py`) with schema version stamping
- Room commands: `/help`, `/who`, `/pause`, `/resume`, `/topic`, `/stats`
- Audit replay summary tool (`src/replay_audit.py`)
- Unit and integration tests for moderator, policy, events, and room behavior
- Documentation suite: roadmap, architecture, API, moderation spec, auditability, onboarding, threat model, ADRs, release docs
- Open-source governance docs: contributing, security, code of conduct
- Tooling baseline: pyproject, Makefile, CI workflow
