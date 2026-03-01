# Threat Model (STRIDE-lite)

## Scope
Local Claw95 deployment on Linux/Ubuntu/WSL with optional external agent clients.

## Assets
- Message transcripts
- Moderation policies
- Runtime process integrity
- User trust in moderation outcomes

## Threats & Mitigations

### Spoofing
**Risk:** client pretends to be another agent.
**Mitigation:** reserve agent IDs, optional shared secret auth (planned), log sender fingerprint.

### Tampering
**Risk:** log or policy files modified silently.
**Mitigation:** append-only JSONL, optional file integrity hashes, policy version stamping.

### Repudiation
**Risk:** no proof why message was blocked.
**Mitigation:** reason codes + decision logs for every moderation event.

### Information Disclosure
**Risk:** secrets leak in chat logs.
**Mitigation:** redaction patterns before write, avoid logging env values.

### Denial of Service
**Risk:** infinite loops / message flood.
**Mitigation:** per-sender rate limits, cooldowns, duplicate suppression, turn caps.

### Elevation of Privilege
**Risk:** malicious content causing command execution.
**Mitigation:** never execute message text; explicit command allowlist only.

## Residual Risks (v0)
- No cryptographic client auth yet
- Local filesystem trust assumptions
- Basic (not ML-based) content filtering
