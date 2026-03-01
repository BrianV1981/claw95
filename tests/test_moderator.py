from copy import deepcopy

from src.moderator import Moderator
from src.policy import DEFAULT_POLICY


def test_blocks_duplicates() -> None:
    p = deepcopy(DEFAULT_POLICY)
    p.cooldown_seconds = 0.0
    m = Moderator(policy=p)
    assert m.evaluate("a", "hello").decision == "ALLOW"
    assert m.evaluate("a", "hello").decision == "BLOCK"


def test_rewrites_long_messages() -> None:
    p = deepcopy(DEFAULT_POLICY)
    p.cooldown_seconds = 0.0
    p.max_message_len = 10
    m = Moderator(policy=p)
    d = m.evaluate("a", "x" * 50)
    assert d.decision == "REWRITE"
    assert len(m.rewrite("x" * 50)) == 10
