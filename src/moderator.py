from __future__ import annotations

import hashlib
import time
from collections import deque, defaultdict
from dataclasses import dataclass


@dataclass
class Decision:
    decision: str
    reason_codes: list[str]


class Moderator:
    """Deterministic policy moderator for room messages."""

    def __init__(
        self,
        cooldown_seconds: float = 2.0,
        duplicate_window: int = 10,
        per_sender_per_min: int = 20,
        max_len: int = 1200,
    ) -> None:
        self.cooldown_seconds = cooldown_seconds
        self.duplicate_window = duplicate_window
        self.per_sender_per_min = per_sender_per_min
        self.max_len = max_len

        self.last_send_ts: dict[str, float] = {}
        self.recent_hashes: deque[str] = deque(maxlen=duplicate_window)
        self.sender_events: dict[str, deque[float]] = defaultdict(deque)

        self.blocked_patterns = ["rm -rf", "DROP TABLE", "sudo reboot"]

    def evaluate(self, sender_id: str, content: str) -> Decision:
        now = time.time()
        clean = (content or "").strip()

        if not sender_id or not clean:
            return Decision("BLOCK", ["MALFORMED"])

        for pattern in self.blocked_patterns:
            if pattern.lower() in clean.lower():
                return Decision("BLOCK", ["POLICY_MATCH"])

        # Rate limit per sender
        events = self.sender_events[sender_id]
        minute_ago = now - 60
        while events and events[0] < minute_ago:
            events.popleft()
        if len(events) >= self.per_sender_per_min:
            return Decision("BLOCK", ["RATE_LIMIT"])

        # Cooldown
        last_ts = self.last_send_ts.get(sender_id)
        if last_ts is not None and now - last_ts < self.cooldown_seconds:
            return Decision("BLOCK", ["COOLDOWN"])

        # Duplicate window
        message_hash = hashlib.sha256(clean.lower().encode("utf-8")).hexdigest()[:16]
        if message_hash in self.recent_hashes:
            return Decision("BLOCK", ["DUPLICATE"])

        # Rewrite overly long messages
        if len(clean) > self.max_len:
            return Decision("REWRITE", ["TOO_LONG"])

        # Update counters on pass/rewrite
        self.last_send_ts[sender_id] = now
        self.recent_hashes.append(message_hash)
        events.append(now)

        return Decision("ALLOW", ["OK"])

    def rewrite(self, content: str) -> str:
        clean = " ".join((content or "").split())
        return clean[: self.max_len]
