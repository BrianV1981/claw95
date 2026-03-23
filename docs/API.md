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
  "topic": "Claw95 POC"
}
```

### `message.published`
```json
{
  "type": "message.published",
  "sender": {"id": "strategist"},
  "content": "Here is my take...",
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
  "command": "pause",
  "ok": true,
  "paused": true,
  "topic": ""
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

Planned but not yet implemented:
- `/summary`
- `/who`
- `/help`
`/topic <text>`

Planned but not yet implemented:
- `/ask <agent>`
- `/summary`
- `/who`
- `/help`
