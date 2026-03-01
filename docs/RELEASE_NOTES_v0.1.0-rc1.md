# Claw95 v0.1.0-rc1 (Draft)

## Highlights
- Deterministic Python moderator with auditable reason codes
- Local WebSocket room server for multi-agent conversations
- Interactive agent bridge client (`/help`, `/who`, `/pause`, `/resume`, `/topic`, `/stats`)
- Configurable policy via `config/policy.yaml`
- JSONL audit logging + replay summary tool

## Engineering Quality
- Linting: Ruff
- Type checking: mypy
- Tests: unit + integration
- CI: GitHub Actions on `main` and `devbranch`

## Documentation
- Architecture, API, moderator spec, auditability guide, threat model, onboarding, roadmap
- CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CHANGELOG, LICENSE

## Known limitations
- No auth on websocket clients yet
- Basic policy engine (no ML/semantic moderation)
- Optional TUI not implemented yet

## Upgrade notes
- Run `pip install -e .[dev]`
- Start server with policy file: `python -m src.server --policy config/policy.yaml`

