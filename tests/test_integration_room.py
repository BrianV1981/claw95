import asyncio
import json
from pathlib import Path

import pytest
from websockets.client import connect
from websockets.server import serve

from src.server import RoomServer


@pytest.mark.asyncio
async def test_room_publish_and_pause(tmp_path: Path) -> None:
    log_file = tmp_path / "events.jsonl"
    policy_file = tmp_path / "policy.yaml"
    policy_file.write_text(
        """
policy_version: "test"
rate_limit:
  per_sender_per_min: 100
cooldown_seconds: 0
duplicate_window: 50
max_message_len: 1200
blocked_patterns: []
room:
  command_prefix: "/"
  start_paused: false
""",
        encoding="utf-8",
    )

    room = RoomServer(log_path=str(log_file), policy_path=str(policy_file))

    async with serve(room.handler, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        uri = f"ws://127.0.0.1:{port}"

        async with connect(uri) as a, connect(uri) as b:
            await a.send(json.dumps({"type": "join", "sender": {"id": "AgentA"}}))
            await b.send(json.dumps({"type": "join", "sender": {"id": "AgentB"}}))

            # Drain initial room.state broadcasts.
            for _ in range(4):
                try:
                    await asyncio.wait_for(a.recv(), timeout=0.2)
                except TimeoutError:
                    break
            for _ in range(4):
                try:
                    await asyncio.wait_for(b.recv(), timeout=0.2)
                except TimeoutError:
                    break

            await a.send(json.dumps({"type": "message.submit", "content": "hello"}))

            seen_published = False
            for _ in range(6):
                evt = json.loads(await asyncio.wait_for(b.recv(), timeout=1))
                if evt.get("type") == "message.published":
                    seen_published = True
                    assert evt["content"] == "hello"
                    break
            assert seen_published

            await a.send(json.dumps({"type": "message.submit", "content": "/pause"}))

            # Drain system message from pause broadcast.
            for _ in range(3):
                evt = json.loads(await asyncio.wait_for(a.recv(), timeout=1))
                if evt.get("type") == "system":
                    break

            await b.send(json.dumps({"type": "message.submit", "content": "still there?"}))
            got_blocked = False
            for _ in range(5):
                evt = json.loads(await asyncio.wait_for(b.recv(), timeout=1))
                if evt.get("type") == "message.blocked":
                    assert evt["decision"]["reason_codes"] == ["ROOM_PAUSED"]
                    got_blocked = True
                    break
            assert got_blocked
