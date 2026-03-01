from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any

from websockets import connect


async def recv_loop(ws: Any) -> None:
    while True:
        evt = json.loads(await ws.recv())
        etype = evt.get("type")
        if etype == "message.published":
            sender = evt.get("sender", {}).get("id", "?")
            content = evt.get("content", "")
            print(f"{sender}> {content}")
        elif etype == "message.blocked":
            print(f"BLOCKED: {evt.get('decision')}")
        elif etype == "room.state":
            users = ", ".join(evt.get("users", []))
            topic = evt.get("topic", "")
            print(f"Users: {users} | Topic: {topic}")
        elif etype == "system":
            print(f"[system] {evt.get('content', '')}")
        else:
            print(evt)


async def send_loop(ws: Any) -> None:
    while True:
        line = await asyncio.to_thread(input, "")
        text = line.strip()
        if not text:
            continue
        await ws.send(json.dumps({"type": "message.submit", "content": text}))


async def run(name: str, uri: str, message: str | None, token: str) -> None:
    async with connect(uri) as ws:
        join_event = {"type": "join", "sender": {"id": name, "type": "agent"}}
        if token:
            join_event["auth"] = {"token": token}
        await ws.send(json.dumps(join_event))

        if message:
            await ws.send(json.dumps({"type": "message.submit", "content": message}))

        print(f"[{name}] connected to {uri}. Type messages or /commands. Ctrl+C to exit.")

        recv_task = asyncio.create_task(recv_loop(ws))
        send_task = asyncio.create_task(send_loop(ws))

        done, pending = await asyncio.wait(
            {recv_task, send_task},
            return_when=asyncio.FIRST_EXCEPTION,
        )
        for task in pending:
            task.cancel()
        for task in done:
            task.result()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawset agent bridge")
    parser.add_argument("--name", required=True)
    parser.add_argument("--uri", default="ws://127.0.0.1:8765")
    parser.add_argument("--message", default=None)
    parser.add_argument("--token", default=os.getenv("CLAW95_TOKEN", ""))
    args = parser.parse_args()

    asyncio.run(run(args.name, args.uri, args.message, args.token))
