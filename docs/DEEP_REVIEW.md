# Deep Review (v0.1.0-rc1)

Date: 2026-03-01
Reviewer: Builder

## Executive summary
Claw95 is in a strong proof-of-concept state with clear architecture, deterministic moderation, and good contributor docs.

**Readiness:** near release candidate for open-source preview.

## What is strong
- Deterministic moderation with reason codes and policy versioning.
- Clear event API and schema stamping (`schema_version`).
- Local-first design is beginner-friendly.
- Auditability path exists (JSONL logs + replay summary tool).
- CI + lint + typing + unit/integration tests are in place.

## Gaps to track (not blockers for preview)
1. **Client authentication**
   - Current room accepts any `sender.id` claim.
   - Recommendation: add optional shared secret or signed token per agent.

2. **Transport security**
   - Defaults to localhost (good), but no TLS mode for remote use.
   - Recommendation: document "localhost only" as security default and add reverse-proxy TLS guide.

3. **Policy depth**
   - Rule-based moderation is intentionally simple.
   - Recommendation: keep deterministic default; add optional semantic review mode later.

4. **Replay tooling depth**
   - Current replay is summary-focused.
   - Recommendation: add filtering (`--reason`, `--sender`, `--from`, `--to`) and CSV export.

5. **Deprecation hygiene**
   - Migrated imports to modern `websockets` entrypoints to reduce warnings.

## Suggested release gate for v0.1.0
- [x] Core room loop functional
- [x] Moderation decisions logged with reason codes
- [x] Policy file configurable
- [x] Commands implemented and documented
- [x] CI passing
- [x] Integration test present
- [ ] Optional: add smoke test script for docs (`scripts/smoke.sh`)

## Final recommendation
Ship `v0.1.0-rc1` as an **open preview** with explicit statement:
- local-first
- unauthenticated prototype transport
- deterministic moderation baseline

Then iterate toward `v0.2.0` on auth and richer audit/replay.
