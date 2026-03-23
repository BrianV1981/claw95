from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


Event = dict[str, Any]


def load_events(path: str | Path, event_type: str | None = None) -> list[Event]:
    file_path = Path(path)
    events: list[Event] = []
    for line in file_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if event_type is not None and row.get("event_type") != event_type:
            continue
        events.append(row)
    return events


def emit_summary(events: list[Event]) -> None:
    for event in events:
        ts = event.get("ts", "?")
        event_type = event.get("event_type", "?")
        sender_id = event.get("sender_id") or event.get("sender", {}).get("id", "-")
        extra = ""
        if "command" in event:
            extra = f" command={event['command']}"
        elif "content" in event:
            extra = f" content={event['content']}"
        print(f"{ts} | {event_type} | sender={sender_id}{extra}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay or inspect Claw95 JSONL event logs")
    parser.add_argument("path", help="Path to JSONL log file")
    parser.add_argument("--event-type", default=None, help="Optional event_type filter")
    args = parser.parse_args()

    events = load_events(args.path, event_type=args.event_type)
    emit_summary(events)


if __name__ == "__main__":
    main()
