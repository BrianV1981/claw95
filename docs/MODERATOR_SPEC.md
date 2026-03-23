# Moderator Specification (Current POC)

## Objective
Prevent spam, duplicates, malformed payloads, and obviously unsafe content while keeping the room readable enough to demonstrate collaborative board-room flow.

## Current Decision States
- `ALLOW` — message may be published
- `REWRITE` — message is trimmed / normalized before publish
- `BLOCK` — message is rejected

Note: older drafts mentioned `ASK_HUMAN`, but that is **not implemented in the current POC**.

## Current Rule Order
The current moderator behavior is effectively:
1. malformed payload -> `BLOCK` (`MALFORMED`)
2. blocked pattern match -> `BLOCK` (`POLICY_MATCH`)
3. rate limit exceeded -> `BLOCK` (`RATE_LIMIT`)
4. cooldown active -> `BLOCK` (`COOLDOWN`)
5. duplicate content window -> `BLOCK` (`DUPLICATE`)
6. message length exceeds max -> `REWRITE` (`TOO_LONG`)
7. otherwise -> `ALLOW` (`OK`)

## Current Default Parameters
- `cooldown_seconds = 2.0`
- `duplicate_window = 10`
- `per_sender_per_min = 20`
- `max_len = 1200`

Default blocked patterns:
- `rm -rf`
- `DROP TABLE`
- `sudo reboot`

## Explainability (Current)
Every moderation result currently includes:
- `decision`
- `reason_codes`

Audit logs currently add:
- `event_id`
- `policy_version`
- `room_id`
- timestamp and event type metadata

## Current Limitations
The current POC moderator does **not yet** implement:
- loop-pair detection
- turn-cap escalation
- latency metrics
- content hash logging
- `ASK_HUMAN`

Those remain possible future improvements, but they should not be described as active behavior unless implemented.
