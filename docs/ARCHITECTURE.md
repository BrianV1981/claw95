# Architecture (Current POC)

## System Overview
Claw95 is currently a local-first real-time AI board-room proof of concept built from three active core components:

1. **Room Server** (`src/server.py`)
   - WebSocket room hub
   - tracks participants and room state
   - processes commands and message publication
   - writes JSONL audit logs

2. **Moderator Engine** (`src/moderator.py`)
   - deterministic message policy engine
   - currently supports `ALLOW`, `REWRITE`, and `BLOCK`
   - enforces malformed checks, cooldown, duplicates, basic policy patterns, and rate limits

3. **Agent Bridge** (`src/agent_bridge.py`)
   - lightweight websocket participant
   - can join the room and print events
   - now supports basic reaction to `room.role_prompt` when the agent role matches

Supporting utility:
4. **Replay / Inspect Utility** (`src/replay.py`)
   - reads JSONL logs
   - filters by `event_type`
   - prints readable summaries for inspection

## POC Scope Reminder
The current POC is meant to prove:
- a visible shared room
- targeted role prompts
- human steering via commands
- deterministic moderation
- basic agent-side reactions
- inspectable logs

It is **not yet** a full orchestration platform or advanced autonomous agent framework.

## Trust Boundaries
- **Untrusted:** inbound message content from users/agents
- **Trusted:** room server state, local moderator rules, local log output
- **Future / not yet implemented:** plugin ecosystems, external tool sandboxes, advanced execution adapters

## Current Event Flow
1. Participant sends `message.submit`
2. Server checks whether the message is a room command
3. If not a command, server routes content through the deterministic moderator
4. If allowed/re-written, server emits `message.published`
5. If `active_target` is set, server also emits `room.role_prompt`
6. Matching agent bridge may submit a deterministic role reply
7. Server logs events to JSONL with metadata such as `event_id`, `policy_version`, and `room_id`

## Current Room State Model
The room currently tracks:
- `users`
- `paused`
- `topic`
- `roles`
- `active_target`
- recent in-memory message history

Default POC roles:
- `strategist`
- `critic`
- `researcher`
- `synthesizer`

## Current Logging Model
JSONL audit rows currently include:
- `event_id`
- `ts`
- `event_type`
- `policy_version`
- `room_id`
- event-specific payload fields

Additional trace fields are present where relevant, including:
- `sender_id`
- `sender_type`
- `command`
- `command_category`

## Reliability / Guardrail Rules (Current)
Implemented today:
- cooldown per sender
- duplicate hash suppression window
- per-sender rate limit
- blocked content patterns
- overlong message rewrite
- paused-room publish blocking

Planned later:
- richer loop detection
- replay helpers beyond simple summary output
- more advanced role behavior

## Security Posture (POC)
- localhost bind by default
- no code execution from room messages
- deterministic moderation path
- inspectable local logs
- minimal dependency surface
