from __future__ import annotations

import asyncio
import json
from typing import Any

from websockets import connect


async def recv_until(ws: Any, wanted: set[str], timeout: float = 2.0) -> dict[str, Any]:
    while True:
        raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
        evt = json.loads(raw)
        if not isinstance(evt, dict):
            continue
        if evt.get("type") in wanted:
            return evt


async def main() -> None:
    uri = "ws://127.0.0.1:8765"
    async with connect(uri) as a, connect(uri) as b:
        await a.send(json.dumps({"type": "join", "sender": {"id": "SmokeA"}}))
        await b.send(json.dumps({"type": "join", "sender": {"id": "SmokeB"}}))

        # drain initial state
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

        await a.send(json.dumps({"type": "message.submit", "content": "hello from smoke"}))
        evt = await recv_until(b, {"message.published"})
        assert evt["type"] == "message.published"

        await a.send(json.dumps({"type": "message.submit", "content": "/pause"}))
        _ = await recv_until(a, {"system"})

        await b.send(json.dumps({"type": "message.submit", "content": "blocked?"}))
        blocked = await recv_until(b, {"message.blocked"})
        assert blocked["decision"]["reason_codes"] == ["ROOM_PAUSED"]

    print("SMOKE_TEST_OK")


if __name__ == "__main__":
    asyncio.run(main())
