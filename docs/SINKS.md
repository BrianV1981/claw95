# Output Sinks

Claw95 can fan out moderated room output to multiple destinations for posterity.

## Supported sinks
1. **JSONL mirror**
2. **Markdown transcript**
3. **Discord webhook archive** (optional)

## Configure in `config/policy.yaml`
```yaml
sinks:
  jsonl_enabled: true
  jsonl_path: "logs/mirror.jsonl"
  markdown_enabled: true
  markdown_path: "logs/transcript.md"
  discord_webhook_url: ""
  discord_webhook_username: "Claw95 Archive"
```

## Notes
- Leave `discord_webhook_url` empty to disable Discord sink.
- Markdown transcript is ideal for Notepad/Notepad++ and wiki imports.
- Sink errors are logged as `sink_error` events and do not crash the room.
