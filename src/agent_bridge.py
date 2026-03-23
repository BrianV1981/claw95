from __future__ import annotations

import argparse
import asyncio
import json
from typing import Any

try:
    from websockets.client import connect
except ModuleNotFoundError:  # pragma: no cover - allows tests without websockets installed
    connect = None


ROLE_PREFIXES = {
    "strategist": "Strategist",
    "critic": "Critic",
    "researcher": "Researcher",
    "synthesizer": "Synthesizer",
}


def build_role_reply(role: str, prompt: str) -> str:
    role_name = ROLE_PREFIXES.get(role, role.title())
    return f"{role_name}: responding to targeted prompt -> {prompt}"


def maybe_build_reply_event(name: str, event: dict[str, Any]) -> dict[str, Any] | None:
    if event.get("type") != "room.role_prompt":
        return None

    role = event.get("role")
    prompt = event.get("prompt", "")
    if role != name:
        return None

    return {
        "type": "message.submit",
        "content": build_role_reply(role, prompt),
    }


async def run(name: str, uri: str, message: str | None) -> None:
    if connect is None:
        raise RuntimeError("websockets is not installed. Install dependencies from requirements.txt first.")

    async with connect(uri) as ws:
        await ws.send(json.dumps({"type": "join", "sender": {"id": name, "type": "agent"}}))

        if message:
            await ws.send(json.dumps({"type": "message.submit", "content": message}))

        print(f"[{name}] connected to {uri}. Ctrl+C to exit.")
        while True:
            evt = json.loads(await ws.recv())
            maybe_reply = maybe_build_reply_event(name, evt)
            if maybe_reply is not None:
                await ws.send(json.dumps(maybe_reply))
                print(f"{name}> {maybe_reply['content']}")
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
    args = parser.parse_args()

    asyncio.run(run(args.name, args.uri, args.message))
