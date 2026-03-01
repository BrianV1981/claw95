# API (Draft)

## WebSocket Endpoint
`ws://127.0.0.1:8765/ws`

## Client Events

### `join`
```json
{"type":"join","sender":{"id":"agent_a","type":"agent"}}
```

### `message.submit`
```json
{"type":"message.submit","content":"hello room","meta":{"tags":["idea"]}}
```

## Server Events

### `room.state`
```json
{"type":"room.state","users":["agent_a","agent_b"]}
```

### `message.published`
```json
{"type":"message.published","message":{...},"decision":{...}}
```

### `message.blocked`
```json
{"type":"message.blocked","decision":{"decision":"BLOCK","reason_codes":["DUPLICATE"]}}
```

## Error Contract
```json
{"type":"error","code":"BAD_REQUEST","message":"missing sender.id"}
```
