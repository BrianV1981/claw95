import unittest

from src.moderator import Moderator


class ModeratorTests(unittest.TestCase):
    def test_blocks_duplicates(self) -> None:
        moderator = Moderator(cooldown_seconds=0)
        self.assertEqual(moderator.evaluate("a", "hello").decision, "ALLOW")
        duplicate = moderator.evaluate("a", "hello")
        self.assertEqual(duplicate.decision, "BLOCK")
        self.assertEqual(duplicate.reason_codes, ["DUPLICATE"])

    def test_rewrites_long_messages(self) -> None:
        moderator = Moderator(cooldown_seconds=0, max_len=10)
        decision = moderator.evaluate("a", "x" * 50)
        self.assertEqual(decision.decision, "REWRITE")
        self.assertEqual(decision.reason_codes, ["TOO_LONG"])
        self.assertEqual(len(moderator.rewrite("x" * 50)), 10)

    def test_blocks_malformed_messages(self) -> None:
        moderator = Moderator(cooldown_seconds=0)
        decision = moderator.evaluate("", "hello")
        self.assertEqual(decision.decision, "BLOCK")
        self.assertEqual(decision.reason_codes, ["MALFORMED"])

    def test_blocks_policy_matches(self) -> None:
        moderator = Moderator(cooldown_seconds=0)
        decision = moderator.evaluate("a", "please run rm -rf /")
        self.assertEqual(decision.decision, "BLOCK")
        self.assertEqual(decision.reason_codes, ["POLICY_MATCH"])

    def test_blocks_cooldown_violations(self) -> None:
        moderator = Moderator(cooldown_seconds=60)
        self.assertEqual(moderator.evaluate("a", "first").decision, "ALLOW")
        decision = moderator.evaluate("a", "second")
        self.assertEqual(decision.decision, "BLOCK")
        self.assertEqual(decision.reason_codes, ["COOLDOWN"])

    def test_blocks_rate_limit_exceeded(self) -> None:
        moderator = Moderator(cooldown_seconds=0, per_sender_per_min=2)
        self.assertEqual(moderator.evaluate("a", "first").decision, "ALLOW")
        self.assertEqual(moderator.evaluate("a", "second").decision, "ALLOW")
        decision = moderator.evaluate("a", "third")
        self.assertEqual(decision.decision, "BLOCK")
        self.assertEqual(decision.reason_codes, ["RATE_LIMIT"])

    def test_rewrite_collapses_whitespace(self) -> None:
        moderator = Moderator(cooldown_seconds=0, max_len=100)
        rewritten = moderator.rewrite("hello   there\n\nfriend")
        self.assertEqual(rewritten, "hello there friend")


if __name__ == "__main__":
    unittest.main()
