# Claw95 POC / MVP PRD

## Working Title
**Claw95 — Real-Time AI Board Room (Proof of Concept)**

## Document Purpose
This document defines the **smallest meaningful proof of concept** for Claw95.

The goal is **not** to build the full product.
The goal is to prove that a live, visible, human-participatory, multi-agent board room is both:
- technically feasible
- meaningfully better than a standard single-agent chat workflow for idea refinement

---

## 1. Product Summary
Claw95 is a **real-time AI board room** where multiple **specialized AI agents** collaborate in one visible shared room while a **human can interject at any time**.

A **deterministic non-AI moderator** controls room order, limits spam, reduces loops, and keeps the conversation readable.

The proof of concept should demonstrate that:
- agent-to-agent discussion can happen live in a shared room
- humans can participate naturally in the same room
- deterministic moderation improves usability
- the resulting discussion produces more useful refinement than a standard one-agent chat

---

## 2. Problem Statement
Most existing AI agent systems focus on:
- hidden orchestration
- task pipelines
- workflow automation
- backend coordination
- post-hoc logs instead of visible discussion

Even when multiple agents are involved, users often cannot:
- watch the discussion unfold in real time
- easily interject inside the same conversation
- understand who is contributing what
- control room behavior with clear deterministic rules

Claw95 aims to solve that by creating a **shared deliberation room**, not just an agent backend.

---

## 3. POC Objective
Build the smallest possible system that proves the following claim:

> A human can get better real-time idea critique and refinement from a visible multi-agent board room with deterministic moderation than from a standard one-agent chat interface.

---

## 4. Primary Use Case
### Core Scenario
A human opens a room, provides an idea/problem/topic, and watches several specialized agents discuss it live.

The human can:
- add clarification
- ask a specific agent a question
- redirect the discussion
- pause/resume the room
- request synthesis

The moderator ensures the room stays readable and prevents low-value failure modes.

### Example POC Topic Types
- business idea critique
- product concept review
- technical planning discussion
- naming / positioning discussion
- pros/cons analysis
- revision/refinement of a proposal

---

## 5. Target User for POC
Primary target user:
- a solo builder / operator / strategist who wants multiple visible AI perspectives in one room

Secondary target users:
- creators refining ideas
- developers planning architecture
- founders reviewing product concepts
- anyone who wants live multi-perspective discussion rather than single-answer generation

---

## 6. What Makes Claw95 Different
The POC must preserve these differentiators:

### 6.1 Live visible collaboration
The user can see the discussion as it happens.

### 6.2 Specialized roles
Agents are not generic bots. Each has a distinct role or lens.

### 6.3 Human in the room
The human is not only an approver outside the loop. The human participates in the same space.

### 6.4 Deterministic moderation
Moderation is handled by explicit non-AI rules, not by another LLM improvising moderation.

### 6.5 Deliberation-first
The system is optimized for critique, review, alternatives, synthesis, and refinement — not just task execution.

---

## 7. POC Scope
## In Scope
The proof of concept must include:

### 7.1 One shared room
- one room is enough for the POC
- local-first operation is acceptable
- browser UI or terminal UI is acceptable

### 7.2 3 to 4 specialized AI agents
Recommended default roles:
- **Strategist** — big-picture framing and opportunity thinking
- **Critic** — identifies weaknesses, risks, contradictions, and gaps
- **Researcher** — adds factual framing, context, assumptions, and needed evidence
- **Synthesizer** — summarizes, merges viewpoints, proposes next-step conclusions

Alternative role sets are acceptable as long as the differentiation between roles is visible.

### 7.3 One human participant
The human must be able to:
- send messages into the same room
- interrupt or redirect discussion
- ask one agent directly
- request summary or next-step synthesis

### 7.4 Real-time message stream
Messages should appear live and visibly in order.
At minimum, each message should show:
- sender name
- timestamp or order
- content

### 7.5 Deterministic moderator
The moderator must operate via explicit logic.
For the POC, the moderator should support at least:
- duplicate suppression
- cooldown between messages
- per-sender rate limit
- max consecutive turns or room turn cap
- loop-risk detection or escalation
- optional rewrite/trim for excessively long content

### 7.6 Minimal room controls
At minimum, the POC should support a small set of commands or controls:
- `/pause`
- `/resume`
- `/ask <agent>`
- `/summary`
- `/topic`

Optional but useful:
- `/round`
- `/who`
- `/help`

### 7.7 Basic audit log
Each event should be written to a simple machine-readable log.
At minimum include:
- timestamp
- sender
- message/event type
- moderator decision
- reason code(s)

---

## 8. Out of Scope for POC
The following should **not** be treated as required for the first proof of concept:

- cloud hosting
- user auth / accounts
- team / org support
- advanced theming
- heavy retro visual polish
- voice support
- Discord/Slack/Matrix bridges
- plugin architecture
- provider abstraction across many vendors
- production-grade persistence architecture
- advanced memory systems
- autonomous workflows / schedulers
- analytics dashboards
- public release engineering

These may be future milestones, but they are not required to prove the concept.

---

## 9. Functional Requirements
### FR1 — Create and run a room
The system must allow a user to launch a room with several agents present.

### FR2 — Agents can post into the room
Agents must be able to send visible messages to the shared room.

### FR3 — Human can post into the room
The human must be able to participate in the same room in real time.

### FR4 — Human can target or redirect discussion
The human must be able to address the room generally or a specific agent directly.

### FR5 — Moderator evaluates all room messages
Every submitted message must pass through the deterministic moderator.

### FR6 — Moderator can ALLOW / REWRITE / BLOCK / ESCALATE
The moderator must make explicit decisions and annotate them.

### FR7 — Room state can be paused/resumed
The human must be able to pause and resume the room.

### FR8 — Room can produce a synthesis
The user must be able to request a summary/synthesis of the current discussion.

### FR9 — Logs are written
All relevant events must be logged in a simple structured format.

---

## 10. Non-Functional Requirements
### NFR1 — Readability
The room must remain readable during normal operation.

### NFR2 — Determinism of moderation
Moderation behavior must be rule-based and explainable.

### NFR3 — Beginner-comprehensible flow
A new user should be able to understand the room model quickly.

### NFR4 — Local-first simplicity
The POC should be easy to run locally with minimal setup.

### NFR5 — Small surface area
The implementation should stay intentionally narrow and avoid premature complexity.

---

## 11. Success Criteria
The POC is successful if the following are true:

### User-experience proof
- A human can launch a room and watch several specialized agents discuss a topic live.
- The human can interject naturally without breaking the flow.
- The room stays understandable and does not collapse into spam.

### Moderation proof
- Duplicate/loop/spam behavior is visibly reduced by the deterministic moderator.
- Moderator decisions can be inspected after the fact.

### Product proof
- The output of the room feels more like collaborative refinement than one-shot answer generation.
- The room produces at least one example where multi-agent interaction adds value over a single-agent answer.

### Scope proof
- The system demonstrates the concept without needing advanced infrastructure or polish.

---

## 12. Failure Conditions
The POC should be considered unsuccessful or incomplete if:
- agents mostly echo each other
- the room becomes unreadable due to spam/loops
- human participation feels bolted on rather than natural
- one hidden “main” agent does all meaningful work
- the moderator does not materially improve room quality
- the result is not clearly better than a standard chatbot session

---

## 13. Recommended POC Architecture Direction
This section is directional, not implementation-binding.

### Suggested shape
- **Room server** — shared event/message hub
- **Moderator** — deterministic rule engine
- **Agent bridge(s)** — lightweight participants representing role-based agents
- **UI** — minimal browser or terminal room interface
- **Audit log** — JSONL or similar append-only event log

The key architectural principle is:
> keep the room visible, keep moderation explicit, keep the implementation small.

---

## 14. Suggested Default Agent Roles
These roles are recommended because they create obvious contrast in the room.

### Strategist
- identifies opportunities
- frames goals and tradeoffs
- pushes toward high-level direction

### Critic
- finds flaws, contradictions, missing assumptions, and risks
- prevents shallow consensus

### Researcher
- adds context, factual framing, uncertainty, and follow-up questions
- identifies what needs verification

### Synthesizer
- consolidates discussion
- proposes structured conclusions and next steps

---

## 15. Example POC Session Flow
1. Human opens room
2. Human enters topic: “Review this product idea”
3. Strategist frames opportunity
4. Critic identifies weaknesses
5. Researcher adds constraints/questions
6. Human interjects with clarification
7. Moderator prevents spam/over-replying
8. Synthesizer summarizes current state
9. Human asks one agent directly
10. Room continues for a bounded number of turns
11. Human requests final summary
12. Audit log preserves the full event trail

---

## 16. Future Milestones (Not POC)
These belong after the concept is validated:
- retro 90s UI polish
- multi-room support
- role template system
- web deployment
- integrations (Discord/Slack/OpenClaw/etc.)
- richer moderation policies
- memory and context persistence
- voice agents
- plugin ecosystem

---

## 17. Final POC Definition
If we strip Claw95 to its essential first proof, it is:

> A local real-time board room where 3–4 specialized AI agents and 1 human discuss ideas in a shared visible room, while a deterministic non-AI moderator keeps the conversation readable and controlled.

That is the proof to build first.
