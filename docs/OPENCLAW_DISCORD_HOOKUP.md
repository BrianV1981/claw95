# OpenClaw + Discord Hookup Guide

This guide explains how to connect Claw95 with your existing OpenClaw Discord setup.

## What you already have
Your `openclaw.json` already includes:
- direct channel -> agent bindings (`builder`, `ops`, `growth`, etc.)
- `agentToAgent.enabled: true`
- `threadBindings.spawnSubagentSessions: true`

So you can orchestrate multi-agent collaboration now.

## Two integration modes

## Mode A — OpenClaw as coordinator (recommended)
- Keep OpenClaw in Discord as your orchestrator.
- Run Claw95 locally for retro room + moderation + sink archiving.
- Mirror key outputs back to Discord using sink webhook.

### Steps
1. Start Claw95 server locally.
2. Set `sinks.discord_webhook_url` in `config/policy.yaml` to a Discord webhook URL.
3. Use OpenClaw in your mission/control channel to coordinate tasks.
4. Paste or relay outputs to Claw95 room participants as needed.

## Mode B — Direct relay script (advanced)
- Build a small bridge script that subscribes to OpenClaw session output and forwards to Claw95 websocket.
- Keep Claw95 as primary transcript + pacing/moderation layer.

## Multi-agent in one Discord room clarification
With one Discord bot token, you get one visible bot identity. You can still run many internal agent brains (orchestrated) but not many visible Discord bot users unless you add multiple bot accounts/tokens.

## Practical prompt to run in mission-control
Use this in your OpenClaw orchestrator channel:

> Run a multi-agent roundtable in this thread with builder, professor, reviewer, and ops.
> Keep responses short. Two rounds max. End with a merged checklist.

Then mirror final output to Claw95 transcript for posterity.
