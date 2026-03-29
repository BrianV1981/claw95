# Claw95 (Synapse)

**Claw95 is an archived architectural testbed for real-time AI collaboration.**

It was originally built as a local-first, multi-agent discussion space where specialized AI participants could collaborate in one visible room, controlled via WebSockets and a deterministic non-AI moderator. 

This repository is the home of the **Claw95 / Synapse proof of concept**, including the archived `aim_swarm.py` and `claw_bridge.py` integration scripts that tested injecting prompts into headless terminal multiplexers (The Phantom Keyboard).

---

## The Historical Significance

Claw95 served as the critical testing ground for the concept of a **Sovereign Swarm**.

Through the development of this repository, we successfully proved that AI agents could be orchestrated to work together by bypassing standard APIs and instead using `tmux send-keys` to spoof human input directly into their REPLs.

However, Claw95 also revealed a critical architectural bottleneck:
Trying to visually pack 4 independent LLM agents into a single 4-way split terminal window while running a local WebSocket server created massive redraw collisions and brittle networking logic. The desire to *visually watch* the room was breaking the underlying logic of the agents.

### The Birth of the Global Chalkboard

The lessons learned from the Claw95 WebSocket experiment led to a massive paradigm shift in the A.I.M. ecosystem. 

By stripping away the UI requirement and the brittle WebSocket layer, the networking model evolved into **The Global Chalkboard Architecture**. Instead of agents talking via WebSockets in a shared UI room, they now communicate asynchronously through atomic, shared documents (like Google Docs or Obsidian files) via the Phantom Keyboard.

## What is in this Archive?

Claw95 is preserved here as a foundational relic. It contains:
- The original room server and deterministic moderator code.
- The `archive_aim_scripts/` folder containing `claw_bridge.py` (the Python-to-WebSocket terminal injector) and `aim_swarm.py` (the local multi-node orchestrator).

This repository can be picked up, dusted off, and brought back to life as its own independent project by anyone who wishes to pursue the local WebSocket "Board Room" paradigm.

---

> *"Treat your AI like a bot, not an oracle. Built by a gamer, for the trenches."*
