from __future__ import annotations

import hashlib
import time
from collections import defaultdict, deque
from dataclasses import dataclass

from .policy import Policy


@dataclass
class Decision:
    decision: str
    reason_codes: list[str]
    policy_version: str


class Moderator:
    """Deterministic policy moderator for room messages."""

    def __init__(self, policy: Policy) -> None:
        self.policy = policy

        self.last_send_ts: dict[str, float] = {}
        self.recent_hashes: deque[str] = deque(maxlen=policy.duplicate_window)
        self.sender_events: dict[str, deque[float]] = defaultdict(deque)

    def evaluate(self, sender_id: str, content: str) -> Decision:
        now = time.time()
        clean = (content or "").strip()

        if not sender_id or not clean:
            return Decision("BLOCK", ["MALFORMED"], self.policy.policy_version)

        for pattern in self.policy.blocked_patterns:
            if pattern.lower() in clean.lower():
                return Decision("BLOCK", ["POLICY_MATCH"], self.policy.policy_version)

        # Rate limit per sender
        events = self.sender_events[sender_id]
        minute_ago = now - 60
        while events and events[0] < minute_ago:
            events.popleft()
        if len(events) >= self.policy.per_sender_per_min:
            return Decision("BLOCK", ["RATE_LIMIT"], self.policy.policy_version)

        # Cooldown
        last_ts = self.last_send_ts.get(sender_id)
        if last_ts is not None and now - last_ts < self.policy.cooldown_seconds:
            return Decision("BLOCK", ["COOLDOWN"], self.policy.policy_version)

        # Duplicate window
        message_hash = hashlib.sha256(clean.lower().encode("utf-8")).hexdigest()[:16]
        if message_hash in self.recent_hashes:
            return Decision("BLOCK", ["DUPLICATE"], self.policy.policy_version)

        # Rewrite overly long messages
        if len(clean) > self.policy.max_message_len:
            # still count it so abuse is rate-limited
            self.last_send_ts[sender_id] = now
            self.recent_hashes.append(message_hash)
            events.append(now)
            return Decision("REWRITE", ["TOO_LONG"], self.policy.policy_version)

        self.last_send_ts[sender_id] = now
        self.recent_hashes.append(message_hash)
        events.append(now)

        return Decision("ALLOW", ["OK"], self.policy.policy_version)

    def rewrite(self, content: str) -> str:
        clean = " ".join((content or "").split())
        return clean[: self.policy.max_message_len]
