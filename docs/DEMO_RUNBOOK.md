# Claw95 Demo Runbook

## Purpose
This runbook demonstrates the current Claw95 proof-of-concept flow end to end:

1. start the room server
2. connect role-based agent bridges
3. connect a human participant
4. target a role
5. trigger a `room.role_prompt`
6. observe the agent bridge reply in the shared room
7. inspect the resulting audit log

This is the fastest way to prove that the current POC behaves like a live AI board room rather than just a static chat server.

---

## Prerequisites
- Python 3.11+
- project dependencies installed
- terminal access to run multiple processes

Optional but recommended:
- one terminal per participant / role bridge

---

## Step 1 — Start the room server
From the repo root:
```bash
python3 -m src.server --host 127.0.0.1 --port 8765 --log logs/events.jsonl
```

Expected output:
```text
Clawset room online at ws://127.0.0.1:8765
```

---

## Step 2 — Start one or more role bridges
Open a new terminal for each role you want to demonstrate.

### Critic
```bash
python3 -m src.agent_bridge --name critic --uri ws://127.0.0.1:8765
```

### Strategist
```bash
python3 -m src.agent_bridge --name strategist --uri ws://127.0.0.1:8765
```

Optional additional roles:
```bash
python3 -m src.agent_bridge --name researcher --uri ws://127.0.0.1:8765
python3 -m src.agent_bridge --name synthesizer --uri ws://127.0.0.1:8765
```

---

## Step 3 — Start a human participant session
Open another terminal and connect as a human-style bridge for manual testing:
```bash
python3 -m src.agent_bridge --name human --uri ws://127.0.0.1:8765
```

Note: the current bridge is a simple websocket participant, so using it as a human terminal is acceptable for the POC.

---

## Step 4 — Set room topic
From the human session, submit:
```json
{"type":"message.submit","content":"/topic Claw95 board room demo"}
```

If you are using the current bridge directly, you may instead start the session with an initial message or use a websocket client that can send raw events.

Expected effect:
- room state reflects the topic
- audit log records the room command

---

## Step 5 — Target a role
Send:
```json
{"type":"message.submit","content":"/ask critic"}
```

Expected effect:
- room state shows `active_target = critic`
- future room messages will carry `target = critic`
- role-aware flow is now armed

---

## Step 6 — Send a targeted prompt
Send:
```json
{"type":"message.submit","content":"Review this launch idea and tell me the biggest weakness."}
```

Expected sequence:
1. room emits `message.published`
2. room emits `room.role_prompt` for `critic`
3. the `critic` bridge receives the prompt and submits a deterministic reply
4. room publishes the critic reply back into the shared room

Expected example reply:
```text
Critic: responding to targeted prompt -> Review this launch idea and tell me the biggest weakness.
```

---

## Step 7 — Use room inspection commands
You can now test:

### Show room summary
```json
{"type":"message.submit","content":"/summary"}
```

### Show participants and roles
```json
{"type":"message.submit","content":"/who"}
```

### Show supported commands
```json
{"type":"message.submit","content":"/help"}
```

---

## Step 8 — Inspect the log output
Replay the JSONL log with the built-in utility:
```bash
python3 -m src.replay logs/events.jsonl
```

Filter to one event type if needed:
```bash
python3 -m src.replay logs/events.jsonl --event-type room_command
python3 -m src.replay logs/events.jsonl --event-type role_prompt
python3 -m src.replay logs/events.jsonl --event-type message_published
```

This is useful for demonstrating:
- room command activity
- moderation and publication flow
- role prompt generation
- traceable event metadata

---

## What This Demo Proves
A successful run demonstrates that Claw95 already has:
- a shared room
- visible multi-party communication
- human steering through commands
- deterministic moderation path
- targeted role prompt generation
- basic agent-side reaction behavior
- inspectable event logs

---

## Current POC Limitations
This demo does **not** yet prove:
- advanced autonomous deliberation
- strong long-context memory between turns
- production-grade UX
- rich replay UI
- sophisticated multi-turn orchestration controls

The room now supports both deterministic bridge replies and local Ollama-backed role participants.
That is acceptable for this stage because the goal is proving the board-room loop and live role handoff, not final intelligence quality.

---

## Recommended Demo Roles
For the clearest demo, use:
- `human`
- `critic`
- `strategist`

That gives you:
- one human operator
- one analytical skeptic
- one high-level planner

---

## Ollama Two-Agent Demo
To prove live AI-to-AI handoff locally with Ollama:

### Terminal 1 — server
```bash
python3 -m src.server --host 127.0.0.1 --port 8772 --log /tmp/claw95-ollama-events.jsonl
```

### Terminal 2 — strategist on Ollama, with handoff to critic
```bash
python3 -m src.agent_bridge \
  --name strategist \
  --uri ws://127.0.0.1:8772 \
  --provider ollama \
  --model llama3.2:latest \
  --next-role critic \
  --handoff-delay-seconds 3.0
```

### Terminal 3 — critic on Ollama
```bash
python3 -m src.agent_bridge \
  --name critic \
  --uri ws://127.0.0.1:8772 \
  --provider ollama \
  --model llama3.2:latest
```

### Terminal 4 — human websocket client or small helper script
Use a websocket client to send:
```json
{"type":"message.submit","content":"/topic both ollama agents"}
{"type":"message.submit","content":"/ask strategist"}
{"type":"message.submit","content":"Propose a launch plan for Claw95, then ask critic to review the biggest operational risks."}
```

Expected proof loop:
1. human prompt is published to `strategist`
2. `strategist` generates a local Ollama reply
3. `strategist` submits first-class handoff (`handoff.submit`) to `critic`
4. server emits `room.handoff` and `room.role_prompt` for `critic`
5. `critic` generates a local Ollama reply

Inspect the resulting log with:
```bash
python3 -m src.replay /tmp/claw95-ollama-events.jsonl --event-type message_published
python3 -m src.replay /tmp/claw95-ollama-events.jsonl --event-type role_prompt
```

## Ollama Three-Agent Demo
To prove a larger board-room chain locally with Ollama:

### Terminal 1 — server
```bash
python3 -m src.server --host 127.0.0.1 --port 8782 --log /tmp/claw95-3agent-events.jsonl
```

### Terminal 2 — strategist on Ollama, handoff to critic
```bash
python3 -m src.agent_bridge \
  --name strategist \
  --uri ws://127.0.0.1:8782 \
  --provider ollama \
  --model llama3.2:latest \
  --next-role critic \
  --handoff-delay-seconds 0.3
```

### Terminal 3 — critic on Ollama, handoff to synthesizer
```bash
python3 -m src.agent_bridge \
  --name critic \
  --uri ws://127.0.0.1:8782 \
  --provider ollama \
  --model llama3.2:latest \
  --next-role synthesizer \
  --handoff-delay-seconds 0.3 \
  --max-turns 1
```

### Terminal 4 — synthesizer on Ollama
```bash
python3 -m src.agent_bridge \
  --name synthesizer \
  --uri ws://127.0.0.1:8782 \
  --provider ollama \
  --model llama3.2:latest
```

### Human prompt
```json
{"type":"message.submit","content":"/topic three agent ollama board room"}
{"type":"message.submit","content":"/ask strategist"}
{"type":"message.submit","content":"Propose a launch plan, have critic review operational risks, then have synthesizer produce a final recommendation."}
```

Expected proof loop:
1. strategist proposes a plan
2. strategist hands off to critic
3. critic reviews risks
4. critic hands off to synthesizer
5. synthesizer produces an integrated recommendation
