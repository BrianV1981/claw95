# Testing Guide

## Automated checks
Run all quality gates:
```bash
make check
```

Equivalent manual commands:
```bash
ruff check .
mypy src tests scripts
pytest -q
```

## Smoke test (end-to-end)
Start the server first, then run:
```bash
python3 scripts/smoke_test.py
```
Expected output:
```text
SMOKE_TEST_OK
```

## Manual chatroom test flow
1. Start server:
   ```bash
   ./scripts/start-dev.sh
   ```
2. Start two clients:
   ```bash
   ./scripts/start-client.sh AgentA
   ./scripts/start-client.sh AgentB
   ```
3. Verify commands in either client:
   - `/help`
   - `/config`
   - `/stats`
   - `/topic test`
   - `/pause`
   - `/resume`
4. Confirm logs are written:
   - `logs/events.jsonl`
   - `logs/mirror.jsonl`
   - `logs/transcript.md`

## Pacing verification
Set in `config/policy.yaml`:
```yaml
room:
  global_min_interval_ms: 1500
```
Then send rapid messages from two clients and confirm output spacing in timestamps.

## Troubleshooting quick checks
- If clients cannot connect: ensure server is running on correct port.
- If `python` fails: use `python3`.
- If transcript is empty: verify sinks enabled in policy.
