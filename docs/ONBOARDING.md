# Newcomer Onboarding (Current POC)

## Fastest Understanding Path
If you are new to Claw95, read these in order:
1. `README.md`
2. `docs/POC_MVP_PRD.md`
3. `docs/WORKFLOW.md`
4. `docs/DEMO_RUNBOOK.md`
5. `docs/NEXT_AGENT_HANDOFF.md`

## Fastest Proof Path
If you want to see the system work quickly:
1. start the room server
2. start one role bridge (for example `critic`)
3. start a human participant
4. set a topic
5. target a role with `/ask`
6. send a prompt
7. inspect the log with `src/replay.py`

## Concepts in Plain English
- **Room server:** the shared live room and command/state hub.
- **Agent bridge:** a participant client that can join, print events, and react to matching role prompts.
- **Moderator:** the deterministic rule engine that decides whether a message is allowed, rewritten, or blocked.
- **Role prompt:** the targeted event emitted when the room is directing a prompt at a specific role.
- **Audit log:** replayable JSONL record of what happened in the room.
- **Replay utility:** a lightweight reader for those JSONL logs.

## Recommended First Exercises
- trigger duplicate suppression
- trigger cooldown block
- set a topic and active target
- trigger a `room.role_prompt`
- watch a matching bridge submit its deterministic reply
- replay the resulting log with `python3 src/replay.py logs/events.jsonl`

## Current Reality Check
The POC is already useful for demonstrating the board-room loop, but it is still intentionally narrow.
Do not assume old aspirational docs describe fully implemented behavior unless they explicitly match the current source-of-truth docs listed above.
