from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib import request


class Sink:
    def publish(self, event: dict[str, Any]) -> None:
        raise NotImplementedError


@dataclass
class JsonlSink(Sink):
    path: Path

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def publish(self, event: dict[str, Any]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


@dataclass
class MarkdownSink(Sink):
    path: Path

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("# Claw95 Transcript\n\n", encoding="utf-8")

    def publish(self, event: dict[str, Any]) -> None:
        if event.get("type") not in {"message.published", "system"}:
            return

        ts = event.get("ts") or datetime.now(UTC).isoformat()
        if event.get("type") == "message.published":
            sender = event.get("sender", {}).get("id", "unknown")
            content = event.get("content", "")
            line = f"- [{ts}] **{sender}**: {content}\n"
        else:
            content = event.get("content", "")
            line = f"- [{ts}] _system_: {content}\n"

        with self.path.open("a", encoding="utf-8") as f:
            f.write(line)


@dataclass
class DiscordWebhookSink(Sink):
    webhook_url: str
    username: str = "Claw95 Archive"

    def publish(self, event: dict[str, Any]) -> None:
        if event.get("type") != "message.published":
            return

        sender = event.get("sender", {}).get("id", "unknown")
        content = str(event.get("content", ""))
        if not content.strip():
            return

        payload = {
            "username": self.username,
            "content": f"[{sender}] {content}"[:1900],
        }
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(req, timeout=3):
            pass


def build_sinks(cfg: dict[str, Any]) -> list[Sink]:
    sinks_cfg = cfg.get("sinks", {})
    sinks: list[Sink] = []

    if bool(sinks_cfg.get("jsonl_enabled", False)):
        sinks.append(JsonlSink(Path(str(sinks_cfg.get("jsonl_path", "logs/mirror.jsonl")))))

    if bool(sinks_cfg.get("markdown_enabled", False)):
        sinks.append(MarkdownSink(Path(str(sinks_cfg.get("markdown_path", "logs/transcript.md")))))

    webhook_url = str(sinks_cfg.get("discord_webhook_url", "")).strip()
    if webhook_url:
        sinks.append(
            DiscordWebhookSink(
                webhook_url=webhook_url,
                username=str(sinks_cfg.get("discord_webhook_username", "Claw95 Archive")),
            )
        )

    return sinks
