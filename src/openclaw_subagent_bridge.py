from __future__ import annotations

import argparse
import asyncio
import json
import re
from dataclasses import dataclass
from pathlib import Path

import yaml
from websockets import connect


@dataclass
class BridgeConfig:
    room_uri: str
    bridge_name: str
    trigger_mode: str
    max_concurrent: int
    request_timeout_seconds: int
    agent_map: dict[str, str]


def load_config(path: str) -> BridgeConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return BridgeConfig(
        room_uri=str(data.get("room_uri", "ws://127.0.0.1:8765")),
        bridge_name=str(data.get("bridge_name", "Bridge")),
        trigger_mode=str(data.get("trigger_mode", "mention")),
        max_concurrent=int(data.get("max_concurrent", 2)),
        request_timeout_seconds=int(data.get("request_timeout_seconds", 120)),
        agent_map={str(k): str(v) for k, v in (data.get("agent_map", {}) or {}).items()},
    )


def parse_targets(text: str, mode: str, names: list[str]) -> list[str]:
    if mode == "all":
        return names

    found: list[str] = []
    lowered = text.lower()
    for name in names:
        if re.search(rf"(^|\s)@{re.escape(name)}(\b|\s|$)", lowered):
            found.append(name)
    return found


def strip_mentions(text: str, names: list[str]) -> str:
    out = text
    for n in names:
        out = re.sub(rf"(^|\s)@{re.escape(n)}(\b)", " ", out, flags=re.IGNORECASE)
    return " ".join(out.split())


async def call_openclaw_agent(agent_id: str, prompt: str, timeout_s: int) -> str:
    proc = await asyncio.create_subprocess_exec(
        "openclaw",
        "sessions",
        "send",
        "--agent",
        agent_id,
        "--message",
        prompt,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    try:
        out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout_s)
    except TimeoutError:
        proc.kill()
        return "[bridge] timeout waiting for subagent"

    if proc.returncode != 0:
        msg = (err.decode("utf-8", errors="ignore") or out.decode("utf-8", errors="ignore")).strip()
        return f"[bridge] subagent error: {msg[:300]}"

    txt = out.decode("utf-8", errors="ignore").strip()
    return txt or "[bridge] empty response"


async def run(config_path: str) -> None:
    cfg = load_config(config_path)
    sem = asyncio.Semaphore(cfg.max_concurrent)

    async with connect(cfg.room_uri) as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "join",
                    "sender": {"id": cfg.bridge_name, "type": "agent"},
                }
            )
        )
        print(f"Bridge connected to {cfg.room_uri} as {cfg.bridge_name}")

        while True:
            evt = json.loads(await ws.recv())
            if evt.get("type") != "message.published":
                continue

            sender = str(evt.get("sender", {}).get("id", ""))
            if sender == cfg.bridge_name:
                continue

            content = str(evt.get("content", "")).strip()
            if not content:
                continue

            targets = parse_targets(content, cfg.trigger_mode, list(cfg.agent_map.keys()))
            if not targets:
                continue

            clean_prompt = strip_mentions(content, list(cfg.agent_map.keys()))

            async def handle_target(target_name: str, prompt_text: str) -> None:
                agent_id = cfg.agent_map[target_name]
                async with sem:
                    reply = await call_openclaw_agent(
                        agent_id,
                        prompt_text,
                        cfg.request_timeout_seconds,
                    )
                    await ws.send(
                        json.dumps(
                            {
                                "type": "message.submit",
                                "content": f"[{target_name}] {reply}",
                            }
                        )
                    )

            await asyncio.gather(*(handle_target(t, clean_prompt) for t in targets))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claw95 OpenClaw subagent bridge")
    parser.add_argument("--config", default="config/subagent_bridge.yaml")
    args = parser.parse_args()

    asyncio.run(run(args.config))
