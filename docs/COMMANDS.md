# Command Reference

Client commands (type inside `agent_bridge.py` sessions):

- `/help` — list available commands
- `/who` — list connected users
- `/topic <text>` — set or show room topic
- `/stats` — show room counters (users/published/blocked/sinks/pacing)
- `/config` — show active moderation + pacing configuration summary
- `/health` — show health summary (uptime, users, sink/auth errors, auth mode, policy hash)
- `/pause` — pause message publishing (messages will be blocked)
- `/resume` — resume message publishing

Notes
- Commands are prefixed with `/` by default (`room.command_prefix`).
- Unknown commands return an error event.
