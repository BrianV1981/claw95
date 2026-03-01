from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def run(path: str) -> None:
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"log not found: {path}")

    counts: Counter[str] = Counter()
    reasons: Counter[str] = Counter()

    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        etype = row.get("event_type", "unknown")
        counts[etype] += 1
        if etype == "moderation_decision":
            for rc in row.get("reason_codes", []):
                reasons[rc] += 1

    print("=== Event counts ===")
    for k, v in counts.most_common():
        print(f"{k:22} {v}")

    if reasons:
        print("\n=== Moderation reason codes ===")
        for k, v in reasons.most_common():
            print(f"{k:22} {v}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replay and summarize Claw95 audit logs")
    parser.add_argument("--log", default="logs/events.jsonl")
    args = parser.parse_args()
    run(args.log)
