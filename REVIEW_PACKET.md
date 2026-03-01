# Review Packet (v0.1.0-rc1 on devbranch)

Use this to validate Claw95 quickly and consistently.

## 0) Update
```bash
cd ~/claw95
git checkout devbranch
git pull
```

## 1) Automated readiness gate
```bash
./scripts/demo-ready.sh
```
Pass criteria:
- preflight PASS
- doctor has 0 FAIL
- smoke test prints `SMOKE_TEST_OK`
- final line: `[demo-ready] PASS`

## 2) Live run
```bash
./scripts/start-room.sh
```
Pass criteria:
- server starts
- AgentA and AgentB connect
- room state prints both users

## 3) Command validation (in client terminal)
Run:
- `/help`
- `/config`
- `/health`
- `/stats`
- `/topic review packet test`

Pass criteria:
- `/help` lists command set
- `/config` shows policy and pacing values
- `/health` shows status=ok + policy hash
- `/stats` includes users/published/blocked/sinks/pace_ms
- topic updates are broadcast

## 4) Moderation/pacing checks
1. Send same message twice
   - expect `DUPLICATE` block on second message
2. `/pause` then send message
   - expect `ROOM_PAUSED` block
3. `/resume` and send message
   - expect publish success
4. rapid two-sender messages
   - verify pacing delay via timestamps if `global_min_interval_ms > 0`

## 5) Sink/log checks
```bash
tail -n 50 logs/events.jsonl

tail -n 50 logs/mirror.jsonl

tail -n 50 logs/transcript.md
```
Pass criteria:
- moderation decisions logged with reason codes
- mirror/transcript populate when enabled

## 6) Optional auth hardening test
Set in `config/policy.yaml`:
```yaml
room:
  shared_secret: "review-secret"
  allowed_senders: ["AgentA", "AgentB"]
```
Restart server.

Test:
- AgentA/AgentB with token -> success
- unknown sender or wrong token -> rejected

## 7) Final sign-off checklist
- [ ] demo-ready PASS
- [ ] commands verified
- [ ] moderation checks verified
- [ ] sink/log checks verified
- [ ] optional auth checks verified (if enabled)

If all checks pass, project is ready for broader user testing / main merge review.
