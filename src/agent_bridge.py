from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
from typing import Any, Callable

try:
    from websockets.asyncio.client import connect
except ModuleNotFoundError:  # pragma: no cover - allows tests without websockets installed
    connect = None


ROLE_PREFIXES = {
    "strategist": "Strategist",
    "critic": "Critic",
    "researcher": "Researcher",
    "synthesizer": "Synthesizer",
}

ROLE_GUIDANCE = {
    "strategist": "Focus on plans, trade-offs, sequencing, and practical next steps.",
    "critic": "Focus on risks, weaknesses, missing assumptions, and operational failure modes.",
    "researcher": "Focus on evidence needs, open questions, validation steps, and factual uncertainty.",
    "synthesizer": "Focus on consensus, key takeaways, tensions between viewpoints, and a clear integrated summary.",
}


def build_role_reply(role: str, prompt: str) -> str:
    role_name = ROLE_PREFIXES.get(role, role.title())
    return f"{role_name}: responding to targeted prompt -> {prompt}"


def build_ollama_prompt(role: str, event: dict[str, Any]) -> str:
    topic = event.get("topic", "")
    prompt = event.get("prompt", "")
    sender = event.get("from_sender", "unknown")
    role_name = ROLE_PREFIXES.get(role, role.title())
    guidance = ROLE_GUIDANCE.get(role, "Stay in role and be specific.")
    return (
        f"You are {role_name} in the Claw95 AI board room. "
        f"Respond as the {role_name} role in 2-5 concise sentences.\n"
        f"Role guidance: {guidance}\n"
        f"Topic: {topic or 'General discussion'}\n"
        f"Prompt from {sender}: {prompt}\n"
        f"Stay in role and be specific."
    )


def generate_reply(role: str, prompt: str, provider: str = "deterministic", model: str | None = None) -> str:
    if provider == "deterministic":
        return build_role_reply(role, prompt)
    if provider != "ollama":
        raise ValueError(f"unsupported provider: {provider}")

    model_name = model or "llama3.2:latest"
    result = subprocess.run(
        ["ollama", "run", model_name, prompt],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def should_respond(turn_count: int, max_turns: int | None) -> bool:
    if max_turns is None:
        return True
    return turn_count < max_turns


def maybe_build_reply_event(name: str, event: dict[str, Any]) -> dict[str, Any] | None:
    events = build_reply_events(name=name, event=event)
    if not events:
        return None
    return events[0]


def build_reply_events(
    name: str,
    event: dict[str, Any],
    provider: str = "deterministic",
    model: str | None = None,
    next_role: str | None = None,
    generate_reply: Callable[[str, str, str, str | None], str] = generate_reply,
) -> list[dict[str, Any]] | None:
    if event.get("type") != "room.role_prompt":
        return None

    role = event.get("role")
    if role != name:
        return None

    if provider == "ollama":
        llm_prompt = build_ollama_prompt(role, event)
        reply_content = generate_reply(role, llm_prompt, provider, model)
    else:
        reply_content = generate_reply(role, event.get("prompt", ""), provider, model)

    events: list[dict[str, Any]] = [{"type": "message.submit", "content": reply_content}]

    if next_role:
        role_name = ROLE_PREFIXES.get(role, role.title())
        events.append(
            {
                "type": "handoff.submit",
                "role": next_role,
                "prompt": f"{role_name} asks {next_role} to respond to: {reply_content}",
            }
        )

    return events


async def run(
    name: str,
    uri: str,
    message: str | None,
    provider: str = "deterministic",
    model: str | None = None,
    next_role: str | None = None,
    handoff_delay_seconds: float = 2.2,
    max_turns: int | None = None,
) -> None:
    if connect is None:
        raise RuntimeError("websockets is not installed. Install dependencies from requirements.txt first.")

    async with connect(uri) as ws:
        await ws.send(json.dumps({"type": "join", "sender": {"id": name, "type": "agent"}}))

        if message:
            await ws.send(json.dumps({"type": "message.submit", "content": message}))

        print(f"[{name}] connected to {uri}. Ctrl+C to exit.")
        turn_count = 0
        while True:
            evt = json.loads(await ws.recv())
            reply_events = build_reply_events(
                name=name,
                event=evt,
                provider=provider,
                model=model,
                next_role=next_role,
            )
            if reply_events is not None:
                if not should_respond(turn_count=turn_count, max_turns=max_turns):
                    print(f"[{name}] max turns reached ({max_turns}); ignoring further role prompts.")
                    continue
                for reply_event in reply_events:
                    await ws.send(json.dumps(reply_event))
                    print(f"{name}> {reply_event['content']}")
                    if reply_event.get("type") == "handoff.submit":
                        await asyncio.sleep(handoff_delay_seconds)
                    else:
                        await asyncio.sleep(0.05)
                turn_count += 1
                continue

            etype = evt.get("type")
            if etype == "message.published":
                sender = evt.get("sender", {}).get("id", "?")
                content = evt.get("content", "")
                print(f"{sender}> {content}")
            elif etype == "message.blocked":
                print(f"BLOCKED: {evt.get('decision')}")
            elif etype == "room.state":
                print(f"Users: {', '.join(evt.get('users', []))}")
            else:
                print(evt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawset agent bridge")
    parser.add_argument("--name", required=True)
    parser.add_argument("--uri", default="ws://127.0.0.1:8765")
    parser.add_argument("--message", default=None)
    parser.add_argument("--provider", choices=["deterministic", "ollama"], default="deterministic")
    parser.add_argument("--model", default=None)
    parser.add_argument("--next-role", default=None)
    parser.add_argument("--handoff-delay-seconds", type=float, default=2.2)
    parser.add_argument("--max-turns", type=int, default=None)
    args = parser.parse_args()

    asyncio.run(
        run(
            name=args.name,
            uri=args.uri,
            message=args.message,
            provider=args.provider,
            model=args.model,
            next_role=args.next_role,
            handoff_delay_seconds=args.handoff_delay_seconds,
            max_turns=args.max_turns,
        )
    )
