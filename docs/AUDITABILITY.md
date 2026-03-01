# Auditability Guide

## Why
Claw95 is designed so each moderation/publish action can be explained after the fact.

## Required Logs
- `message_received`
- `moderation_decision`
- `message_published` or `message_blocked`
- `room_command`

## Log Format
JSONL (one event per line), append-only.

## Minimum Fields
- `event_id`
- `timestamp`
- `room_id`
- `sender_id`
- `event_type`
- `decision`
- `reason_codes`
- `policy_version`

## Operational Checklist
- Verify clock sync
- Verify log write permissions
- Verify redaction enabled
- Verify policy version stamped
