import json
import unittest

from src.agent_bridge import build_role_reply, maybe_build_reply_event


class AgentBridgeTests(unittest.TestCase):
    def test_build_role_reply_uses_role_voice(self) -> None:
        reply = build_role_reply("critic", "Review this launch plan")
        self.assertIn("Critic", reply)
        self.assertIn("Review this launch plan", reply)

    def test_maybe_build_reply_event_returns_none_for_unrelated_events(self) -> None:
        event = {"type": "message.published", "content": "hello"}
        self.assertIsNone(maybe_build_reply_event("critic", event))

    def test_maybe_build_reply_event_returns_none_for_other_role(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "strategist",
            "prompt": "Review this launch plan",
        }
        self.assertIsNone(maybe_build_reply_event("critic", event))

    def test_maybe_build_reply_event_returns_message_for_matching_role(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "critic",
            "prompt": "Review this launch plan",
        }
        reply = maybe_build_reply_event("critic", event)
        self.assertIsNotNone(reply)
        assert reply is not None
        self.assertEqual(reply["type"], "message.submit")
        self.assertIn("Critic", reply["content"])
        self.assertIn("Review this launch plan", reply["content"])


if __name__ == "__main__":
    unittest.main()
