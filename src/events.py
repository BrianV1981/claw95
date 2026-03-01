from __future__ import annotations

from typing import Any

SCHEMA_VERSION = "1.0"


def validate_inbound_event(event: dict[str, Any]) -> tuple[bool, str | None]:
    etype = event.get("type")
    if not isinstance(etype, str):
        return False, "missing event type"

    if etype == "join":
        sender = event.get("sender", {})
        if not isinstance(sender, dict) or not sender.get("id"):
            return False, "join requires sender.id"
        return True, None

    if etype == "message.submit":
        content = event.get("content")
        if not isinstance(content, str):
            return False, "message.submit requires string content"
        return True, None

    return False, f"unknown event type: {etype}"
