import asyncio
import json
from pathlib import Path

import pytest
from websockets import connect, serve

from src.server import RoomServer


@pytest.mark.asyncio
async def test_join_auth_required(tmp_path: Path) -> None:
    log_file = tmp_path / "events.jsonl"
    policy_file = tmp_path / "policy.yaml"
    policy_file.write_text(
        '''
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
  shared_secret: "secret123"
''',
        encoding="utf-8",
    )

    room = RoomServer(log_path=str(log_file), policy_path=str(policy_file))

    async with serve(room.handler, "127.0.0.1", 0) as server:
        port = server.sockets[0].getsockname()[1]
        uri = f"ws://127.0.0.1:{port}"

        async with connect(uri) as ws:
            await ws.send(json.dumps({"type": "join", "sender": {"id": "Bad"}}))
            evt = json.loads(await asyncio.wait_for(ws.recv(), timeout=1))
            assert evt["type"] == "error"
            assert evt["message"] == "auth failed"

        async with connect(uri) as ws2:
            await ws2.send(
                json.dumps(
                    {
                        "type": "join",
                        "sender": {"id": "Good"},
                        "auth": {"token": "secret123"},
                    }
                )
            )
            evt = json.loads(await asyncio.wait_for(ws2.recv(), timeout=1))
            assert evt["type"] == "room.state"
            assert "Good" in evt["users"]
