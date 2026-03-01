from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class Policy:
    policy_version: str
    per_sender_per_min: int
    cooldown_seconds: float
    duplicate_window: int
    max_message_len: int
    blocked_patterns: list[str]
    command_prefix: str
    start_paused: bool
    global_min_interval_ms: int
    shared_secret: str
    sinks: dict[str, object]


DEFAULT_POLICY = Policy(
    policy_version="2026.03.01",
    per_sender_per_min=20,
    cooldown_seconds=2.0,
    duplicate_window=10,
    max_message_len=1200,
    blocked_patterns=["rm -rf", "DROP TABLE", "sudo reboot"],
    command_prefix="/",
    start_paused=False,
    global_min_interval_ms=0,
    shared_secret="",
    sinks={
        "jsonl_enabled": False,
        "jsonl_path": "logs/mirror.jsonl",
        "markdown_enabled": False,
        "markdown_path": "logs/transcript.md",
        "discord_webhook_url": "",
        "discord_webhook_username": "Claw95 Archive",
    },
)


def load_policy(path: str | Path) -> Policy:
    p = Path(path)
    if not p.exists():
        return DEFAULT_POLICY

    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}

    rate = data.get("rate_limit", {})
    room = data.get("room", {})
    sinks = data.get("sinks", {})

    default_sinks = dict(DEFAULT_POLICY.sinks)
    if isinstance(sinks, dict):
        default_sinks.update(sinks)

    return Policy(
        policy_version=str(data.get("policy_version", DEFAULT_POLICY.policy_version)),
        per_sender_per_min=int(rate.get("per_sender_per_min", DEFAULT_POLICY.per_sender_per_min)),
        cooldown_seconds=float(data.get("cooldown_seconds", DEFAULT_POLICY.cooldown_seconds)),
        duplicate_window=int(data.get("duplicate_window", DEFAULT_POLICY.duplicate_window)),
        max_message_len=int(data.get("max_message_len", DEFAULT_POLICY.max_message_len)),
        blocked_patterns=list(data.get("blocked_patterns", DEFAULT_POLICY.blocked_patterns)),
        command_prefix=str(room.get("command_prefix", DEFAULT_POLICY.command_prefix)),
        start_paused=bool(room.get("start_paused", DEFAULT_POLICY.start_paused)),
        global_min_interval_ms=int(
            room.get("global_min_interval_ms", DEFAULT_POLICY.global_min_interval_ms)
        ),
        shared_secret=str(room.get("shared_secret", DEFAULT_POLICY.shared_secret)),
        sinks=default_sinks,
    )
