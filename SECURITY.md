# Security Policy

## Supported Versions
Pre-1.0 releases are experimental but security issues are handled promptly.

## Reporting
Please report vulnerabilities privately via security contact in repository settings.
Do not open public issues for active exploits.

## Security Principles
- Least privilege
- Local-first defaults
- Explicit trust boundaries
- Auditable moderation decisions

## Known Risk Areas
- Prompt injection in agent messages
- Infinite response loops
- Unsafe command text passing through agent bridges
- Secrets leakage in logs

## Mitigations (v0)
- deterministic moderator before publish
- command allowlist
- duplicate and loop guard
- sensitive token redaction in logs
