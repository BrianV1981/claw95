from __future__ import annotations

import argparse
import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from websockets.server import WebSocketServerProtocol, serve

from moderator import Moderator


class RoomServer:
    def __init__(self, log_path: str = "logs/events.jsonl") -> None:
        self.clients: set[WebSocketServerProtocol] = set()
        self.usernames: dict[WebSocketServerProtocol, str] = {}
        self.moderator = Moderator()
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def _log(self, event_type: str, payload: dict[str, Any]) -> None:
        row = {
            "ts": datetime.now(UTC).isoformat(),
            "event_type": event_type,
            **payload,
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    async def _broadcast(self, msg: dict[str, Any]) -> None:
        dead = []
        wire = json.dumps(msg, ensure_ascii=False)
        for client in self.clients:
            try:
                await client.send(wire)
            except Exception:
                dead.append(client)
        for d in dead:
            self.clients.discard(d)
            self.usernames.pop(d, None)

    async def handler(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        try:
            async for raw in ws:
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    await ws.send(json.dumps({"type": "error", "message": "invalid json"}))
                    continue

                etype = event.get("type")
                if etype == "join":
                    sender_id = event.get("sender", {}).get("id", "anon")
                    self.usernames[ws] = sender_id
                    self._log("join", {"sender_id": sender_id})
                    await self._broadcast(
                        {"type": "room.state", "users": list(self.usernames.values())}
                    )
                    continue

                if etype == "message.submit":
                    sender_id = self.usernames.get(ws, "anon")
                    content = event.get("content", "")
                    decision = self.moderator.evaluate(sender_id, content)
                    self._log(
                        "moderation_decision",
                        {
                            "sender_id": sender_id,
                            "decision": decision.decision,
                            "reason_codes": decision.reason_codes,
                            "content": content,
                        },
                    )

                    if decision.decision == "BLOCK":
                        await ws.send(
                            json.dumps(
                                {
                                    "type": "message.blocked",
                                    "decision": {
                                        "decision": decision.decision,
                                        "reason_codes": decision.reason_codes,
                                    },
                                }
                            )
                        )
                        continue

                    if decision.decision == "REWRITE":
                        content = self.moderator.rewrite(content)

                    outbound = {
                        "type": "message.published",
                        "sender": {"id": sender_id},
                        "content": content,
                        "decision": {
                            "decision": decision.decision,
                            "reason_codes": decision.reason_codes,
                        },
                    }
                    self._log("message_published", outbound)
                    await self._broadcast(outbound)

        finally:
            self.clients.discard(ws)
            self.usernames.pop(ws, None)
            await self._broadcast({"type": "room.state", "users": list(self.usernames.values())})


async def main(host: str, port: int, log_path: str) -> None:
    room = RoomServer(log_path=log_path)
    async with serve(room.handler, host, port):
        print(f"Clawset room online at ws://{host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawset Room Server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--log", default="logs/events.jsonl")
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.log))
