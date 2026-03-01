from __future__ import annotations

import argparse
import asyncio
import json

from websockets.client import connect


async def run(name: str, uri: str, message: str | None) -> None:
    async with connect(uri) as ws:
        await ws.send(json.dumps({"type": "join", "sender": {"id": name, "type": "agent"}}))

        if message:
            await ws.send(json.dumps({"type": "message.submit", "content": message}))

        print(f"[{name}] connected to {uri}. Ctrl+C to exit.")
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
