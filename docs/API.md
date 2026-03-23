# API (POC Draft)

## WebSocket Endpoint
`ws://127.0.0.1:8765`

## Client Events

### `join`
```json
{"type":"join","sender":{"id":"human","type":"human"}}
```

### `message.submit`
```json
{"type":"message.submit","content":"hello room"}
```

Commands are sent through normal `message.submit` content:
```json
{"type":"message.submit","content":"/pause"}
```

## Server Events

### `room.state`
```json
{
  "type": "room.state",
  "users": ["human", "strategist"],
  "paused": false,
  "topic": "Claw95 POC",
  "roles": ["strategist", "critic", "researcher", "synthesizer"],
  "active_target": "strategist"
}
```

### `message.published`
```json
{
  "type": "message.published",
  "sender": {"id": "strategist"},
  "content": "Here is my take...",
  "target": "critic",
  "decision": {
    "decision": "ALLOW",
    "reason_codes": ["OK"]
  }
}
```

### `message.blocked`
```json
{
  "type": "message.blocked",
  "decision": {
    "decision": "BLOCK",
    "reason_codes": ["DUPLICATE"]
  }
}
```

### `room.command.result`
```json
{
  "type": "room.command.result",
  "command": "ask",
  "ok": true,
  "paused": false,
  "topic": "Claw95 POC",
  "active_target": "strategist"
}
```

### `room.summary`
```json
{
  "type": "room.summary",
  "paused": false,
  "topic": "Claw95 POC",
  "active_target": "strategist",
  "roles": ["strategist", "critic", "researcher", "synthesizer"],
  "recent_messages_count": 2,
  "recent_messages": [
    {
      "sender_id": "human",
      "content": "first idea",
      "target": "strategist",
      "decision": "ALLOW"
    }
  ]
}
```

## Audit Log Row (JSONL)
Every logged event includes stable metadata:
```json
{
  "event_id": "5d9ff5ce-66c0-418f-8eb4-e5a3fef8ebd4",
  "ts": "2026-03-23T10:00:00.000000+00:00",
  "event_type": "room_command",
  "policy_version": "poc-v1",
  "sender_id": "human",
  "command": "pause"
}
```

### `room.who`
```json
{
  "type": "room.who",
  "users": ["human"],
  "roles": ["strategist", "critic", "researcher", "synthesizer"],
  "active_target": "strategist",
  "paused": false,
  "topic": "Claw95 POC"
}
```

### `room.help`
```json
{
  "type": "room.help",
  "commands": [
    "/pause",
    "/resume",
    "/topic <text>",
    "/ask <agent>",
    "/summary",
    "/who",
    "/help"
  ]
}
```

### `error`
```json
{"type":"error","code":"UNKNOWN_COMMAND","message":"unknown command: /whatever"}
```

## Current POC Commands
- `/pause`
- `/resume`
- `/topic <text>`
- `/ask <agent>`
- `/summary`
- `/who`
- `/help`
