from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from websockets.server import WebSocketServerProtocol, serve

from .events import SCHEMA_VERSION, validate_inbound_event
from .moderator import Moderator
from .policy import load_policy


class RoomServer:
    def __init__(self, log_path: str, policy_path: str) -> None:
        self.clients: set[WebSocketServerProtocol] = set()
        self.usernames: dict[WebSocketServerProtocol, str] = {}
        self.policy = load_policy(policy_path)
        self.moderator = Moderator(self.policy)
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.command_prefix = self.policy.command_prefix
        self.paused = self.policy.start_paused
        self.topic = "Welcome to The Clawset"

        self.messages_published = 0
        self.messages_blocked = 0

    def _log(self, event_type: str, payload: dict[str, Any]) -> None:
        row = {
            "schema_version": SCHEMA_VERSION,
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

    async def _send_system(self, ws: WebSocketServerProtocol, content: str) -> None:
        await ws.send(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "system",
                    "content": content,
                }
            )
        )

    async def _handle_command(
        self,
        ws: WebSocketServerProtocol,
        sender_id: str,
        content: str,
    ) -> None:
        rest = content[len(self.command_prefix) :].strip()
        cmd, _, arg = rest.partition(" ")
        cmd = cmd.lower()

        if cmd == "help":
            await self._send_system(
                ws,
                "Commands: /help, /who, /pause, /resume, /topic <text>, /stats",
            )
            return

        if cmd == "who":
            users = ", ".join(self.usernames.values())
            await self._send_system(ws, f"Users: {users}")
            return

        if cmd == "pause":
            self.paused = True
            self._log("room_command", {"sender_id": sender_id, "command": "pause"})
            await self._broadcast(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "system",
                    "content": "Room is now paused.",
                }
            )
            return

        if cmd == "resume":
            self.paused = False
            self._log("room_command", {"sender_id": sender_id, "command": "resume"})
            await self._broadcast(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "system",
                    "content": "Room resumed.",
                }
            )
            return

        if cmd == "topic":
            if not arg.strip():
                await self._send_system(ws, f"Current topic: {self.topic}")
                return
            self.topic = arg.strip()[:200]
            self._log(
                "room_command",
                {
                    "sender_id": sender_id,
                    "command": "topic",
                    "topic": self.topic,
                },
            )
            await self._broadcast(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "system",
                    "content": f"Topic set by {sender_id}: {self.topic}",
                }
            )
            return

        if cmd == "stats":
            stats = (
                f"users={len(self.usernames)} | published={self.messages_published} "
                f"| blocked={self.messages_blocked} | paused={self.paused}"
            )
            await self._send_system(ws, stats)
            return

        await ws.send(
            json.dumps(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "error",
                    "message": f"unknown command: {cmd}",
                }
            )
        )

    async def handler(self, ws: WebSocketServerProtocol) -> None:
        self.clients.add(ws)
        try:
            async for raw in ws:
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    await ws.send(
                        json.dumps(
                            {
                                "schema_version": SCHEMA_VERSION,
                                "type": "error",
                                "message": "invalid json",
                            }
                        )
                    )
                    continue

                valid, err = validate_inbound_event(event)
                if not valid:
                    await ws.send(
                        json.dumps(
                            {
                                "schema_version": SCHEMA_VERSION,
                                "type": "error",
                                "message": err,
                            }
                        )
                    )
                    continue

                etype = event.get("type")
                if etype == "join":
                    sender_id = str(event.get("sender", {}).get("id", "anon"))
                    self.usernames[ws] = sender_id
                    self._log("join", {"sender_id": sender_id})
                    await self._broadcast(
                        {
                            "schema_version": SCHEMA_VERSION,
                            "type": "room.state",
                            "users": list(self.usernames.values()),
                            "topic": self.topic,
                        }
                    )
                    continue

                if etype == "message.submit":
                    sender_id = self.usernames.get(ws, "anon")
                    content = str(event.get("content", ""))

                    if content.startswith(self.command_prefix):
                        await self._handle_command(ws, sender_id, content)
                        continue

                    if self.paused:
                        self.messages_blocked += 1
                        await ws.send(
                            json.dumps(
                                {
                                    "schema_version": SCHEMA_VERSION,
                                    "type": "message.blocked",
                                    "decision": {
                                        "decision": "BLOCK",
                                        "reason_codes": ["ROOM_PAUSED"],
                                    },
                                }
                            )
                        )
                        continue

                    decision = self.moderator.evaluate(sender_id, content)
                    self._log(
                        "moderation_decision",
                        {
                            "sender_id": sender_id,
                            "decision": decision.decision,
                            "reason_codes": decision.reason_codes,
                            "policy_version": decision.policy_version,
                            "content_hash": hashlib.sha256(
                                content.encode("utf-8")
                            ).hexdigest()[:16],
                        },
                    )

                    if decision.decision == "BLOCK":
                        self.messages_blocked += 1
                        await ws.send(
                            json.dumps(
                                {
                                    "schema_version": SCHEMA_VERSION,
                                    "type": "message.blocked",
                                    "decision": {
                                        "decision": decision.decision,
                                        "reason_codes": decision.reason_codes,
                                        "policy_version": decision.policy_version,
                                    },
                                }
                            )
                        )
                        continue

                    if decision.decision == "REWRITE":
                        content = self.moderator.rewrite(content)

                    self.messages_published += 1
                    outbound = {
                        "schema_version": SCHEMA_VERSION,
                        "type": "message.published",
                        "sender": {"id": sender_id},
                        "content": content,
                        "topic": self.topic,
                        "decision": {
                            "decision": decision.decision,
                            "reason_codes": decision.reason_codes,
                            "policy_version": decision.policy_version,
                        },
                    }
                    self._log("message_published", outbound)
                    await self._broadcast(outbound)

        finally:
            self.clients.discard(ws)
            self.usernames.pop(ws, None)
            await self._broadcast(
                {
                    "schema_version": SCHEMA_VERSION,
                    "type": "room.state",
                    "users": list(self.usernames.values()),
                    "topic": self.topic,
                }
            )


async def main(host: str, port: int, log_path: str, policy_path: str) -> None:
    room = RoomServer(log_path=log_path, policy_path=policy_path)
    async with serve(room.handler, host, port):
        print(f"Clawset room online at ws://{host}:{port}")
        print(f"Policy loaded from: {policy_path}")
        await asyncio.Future()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clawset Room Server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--log", default="logs/events.jsonl")
    parser.add_argument("--policy", default="config/policy.yaml")
    args = parser.parse_args()
    asyncio.run(main(args.host, args.port, args.log, args.policy))
