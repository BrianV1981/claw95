# ADR-0001: Deterministic Moderation First

## Status
Accepted

## Context
The project targets newcomers and needs auditability and predictable behavior.
Early LLM-only moderation is hard to test and explain.

## Decision
Implement a deterministic Python policy engine as the default moderator in v0.x.

## Consequences
### Positive
- Fast and cheap moderation
- Repeatable tests
- Clear reason codes for every decision

### Negative
- Lower nuance than LLM moderation
- Requires manual updates for new policy patterns

## Follow-up
Add optional LLM-assisted fallback for `ASK_HUMAN` in v0.2+.
