# START HERE

If you only read one file, read this.

## 60-second setup
```bash
git clone https://github.com/BrianV1981/claw95.git
cd claw95
git checkout devbranch
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Preflight check (recommended)
```bash
./scripts/preflight.sh
```

## Doctor check (runtime + sink readiness)
```bash
./scripts/doctor.sh
```

## Demo-ready gate (all-in-one)
```bash
./scripts/demo-ready.sh
```

## Launch room + clients
Simplest reliable mode (recommended):
```bash
./scripts/start-safe.sh
```
This starts **server only** and prints exact commands for AgentA/AgentB in separate terminals.

Optional one-command tmux mode:
```bash
./scripts/dev-stack.sh
```
Then attach:
```bash
tmux attach -t claw95
```
This gives server + AgentA + AgentB in panes.

Quick watch mode:
```bash
./scripts/start-room.sh
```
This runs server + two watch clients (no stdin input mode).

Manual 3-terminal mode:

Terminal 1:
```bash
./scripts/start-dev.sh
```

Terminal 2:
```bash
./scripts/start-client.sh AgentA
```

Terminal 3:
```bash
./scripts/start-client.sh AgentB
```

## Validate quickly
Type in a client:
- `/help`
- `/config`
- `/health`
- `/stats`
- `/topic hello`

Then run:
```bash
python3 scripts/smoke_test.py
```
Expected: `SMOKE_TEST_OK`

## Where to look next
- `QUICKSTART.md` — full setup + troubleshooting
- `docs/COMMANDS.md` — command reference
- `docs/OPERATIONS.md` — runtime operations
- `docs/TESTING.md` — validation workflow
