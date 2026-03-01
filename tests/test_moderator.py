from src.moderator import Moderator


def test_blocks_duplicates() -> None:
    m = Moderator(cooldown_seconds=0)
    assert m.evaluate("a", "hello").decision == "ALLOW"
    assert m.evaluate("a", "hello").decision == "BLOCK"


def test_rewrites_long_messages() -> None:
    m = Moderator(cooldown_seconds=0, max_len=10)
    d = m.evaluate("a", "x" * 50)
    assert d.decision == "REWRITE"
    assert len(m.rewrite("x" * 50)) == 10
