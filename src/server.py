from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from websockets.server import WebSocketServerProtocol, serve
except ModuleNotFoundError:  # pragma: no cover - allows unit tests without websockets installed
    WebSocketServerProtocol = Any  # type: ignore[assignment]
    serve = None

from src.moderator import Moderator


class RoomServer:
    def __init__(self, log_path: str = "logs/events.jsonl") -> None:
        self.clients: set[WebSocketServerProtocol] = set()
        self.usernames: dict[WebSocketServerProtocol, str] = {}
        self.moderator = Moderator()
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.paused = False
        self.topic = ""
        self.roles = ["strategist", "critic", "researcher", "synthesizer"]
        self.active_target: str | None = None

    def _log(self, event_type: str, payload: dict[str, Any]) -> None:
        row = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            **payload,
        }
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def _room_state(self) -> dict[str, Any]:
        return {
            "type": "room.state",
            "users": list(self.usernames.values()),
            "paused": self.paused,
            "topic": self.topic,
            "roles": self.roles,
            "active_target": self.active_target,
        }

    async def _broadcast(self, msg: dict[str, Any]) -> None:
        dead = []
        wire = json.dumps(msg, ensure_ascii=False)
        for client in self.clients:
            try:
                await client.send(wire)
            except Exception:
                dead.append(client)
        for dead_client in dead:
            self.clients.discard(dead_client)
            self.usernames.pop(dead_client, None)

    async def _send(self, ws: WebSocketServerProtocol, msg: dict[str, Any]) -> None:
        await ws.send(json.dumps(msg, ensure_ascii=False))

    def _parse_command(self, content: str) -> tuple[str, str] | None:
        clean = (content or "").strip()
        if not clean.startswith("/"):
            return None
        body = clean[1:]
        command, _, argument = body.partition(" ")
        return command.lower(), argument.strip()

    async def _handle_command(self, ws: WebSocketServerProtocol, sender_id: str, command: str, argument: str) -> None:
        if command == "pause":
            self.paused = True
        elif command == "resume":
            self.paused = False
        elif command == "topic":
            self.topic = argument
        elif command == "ask":
            if not argument or argument not in self.roles:
                await self._send(
                    ws,
                    {
                        "type": "error",
                        "code": "UNKNOWN_AGENT",
                        "message": f"unknown agent: {argument or '<missing>'}",
                        "roles": self.roles,
                    },
                )
                return
            self.active_target = argument
        else:
            await self._send(
                ws,
                {
                    "type": "error",
                    "code": "UNKNOWN_COMMAND",
                    "message": f"unknown command: /{command}",
                },
            )
            return

        self._log(
            "room_command",
            {
                "sender_id": sender_id,
                "command": command,
                "argument": argument,
                "paused": self.paused,
                "topic": self.topic,
                "active_target": self.active_target,
            },
        )
        await self._send(
            ws,
            {
                "type": "room.command.result",
                "command": command,
                "ok": True,
                "paused": self.paused,
                "topic": self.topic,
                "active_target": self.active_target,
            },
        )
        await self._broadcast(self._room_state())

    async def handle_event(self, ws: WebSocketServerProtocol, event: dict[str, Any]) -> None:
        etype = event.get("type")
        if etype == "join":
            sender_id = event.get("sender", {}).get("id", "anon")
            self.usernames[ws] = sender_id
            self._log("join", {"sender_id": sender_id})
            await self._broadcast(self._room_state())
            return

        if etype != "message.submit":
            await self._send(ws, {"type": "error", "code": "BAD_REQUEST", "message": "unsupported event type"})
            return

        sender_id = self.usernames.get(ws, "anon")
        content = event.get("content", "")
        command = self._parse_command(content)
        if command is not None:
            command_name, argument = command
            await self._handle_command(ws, sender_id, command_name, argument)
            return

        if self.paused:
            await self._send(
                ws,
                {
                    "type": "message.blocked",
                    "decision": {"decision": "BLOCK", "reason_codes": ["PAUSED"]},
                },
            )
            return

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
            await self._send(
                ws,
                {
                    "type": "message.blocked",
                    "decision": {
                        "decision": decision.decision,
                        "reason_codes": decision.reason_codes,
                    },
                },
            )
            return

        if decision.decision == "REWRITE":
            content = self.moderator.rewrite(content)

        outbound = {
            "type": "message.published",
            "sender": {"id": sender_id},
            "content": content,
            "target": self.active_target,
            "decision": {
                "decision": decision.decision,
                "reason_codes": decision.reason_codes,
            },
        }
        self._log("message_published", outbound)
        await self._broadcast(outbound)

    async def handler(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        try:
            async for raw in ws:
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    await self._send(ws, {"type": "error", "message": "invalid json"})
                    continue
                await self.handle_event(ws, event)
        finally:
            self.clients.discard(ws)
            self.usernames.pop(ws, None)
            await self._broadcast(self._room_state())


async def main(host: str, port: int, log_path: str) -> None:
    if serve is None:
        raise RuntimeError("websockets is not installed. Install dependencies from requirements.txt first.")
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
