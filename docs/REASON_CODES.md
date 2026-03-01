# Moderation Reason Codes

Canonical reason codes used by the deterministic moderator:

- `OK` — message allowed
- `MALFORMED` — missing sender/content
- `POLICY_MATCH` — blocked pattern match
- `RATE_LIMIT` — per-sender message cap exceeded
- `COOLDOWN` — sender posted too quickly
- `DUPLICATE` — duplicate content in recent window
- `TOO_LONG` — message rewritten due to max length
- `ROOM_PAUSED` — room paused by moderator command

These codes are logged in `moderation_decision` events for auditability.
