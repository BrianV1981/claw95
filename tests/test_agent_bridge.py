import unittest

from src.agent_bridge import (
    build_ollama_prompt,
    build_reply_events,
    build_role_reply,
    maybe_build_reply_event,
    should_respond,
)


class AgentBridgeTests(unittest.TestCase):
    def test_build_role_reply_uses_role_voice(self) -> None:
        reply = build_role_reply("critic", "Review this launch plan")
        self.assertIn("Critic", reply)
        self.assertIn("Review this launch plan", reply)

    def test_build_ollama_prompt_includes_role_and_topic(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "critic",
            "prompt": "Review this launch plan",
            "topic": "Launch review",
            "from_sender": "human",
        }
        prompt = build_ollama_prompt("critic", event)
        self.assertIn("critic", prompt.lower())
        self.assertIn("Launch review", prompt)
        self.assertIn("Review this launch plan", prompt)

    def test_build_ollama_prompt_includes_role_specific_guidance(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "critic",
            "prompt": "Review this launch plan",
            "topic": "Launch review",
            "from_sender": "human",
        }
        critic_prompt = build_ollama_prompt("critic", event)
        strategist_prompt = build_ollama_prompt("strategist", event)
        synthesizer_prompt = build_ollama_prompt("synthesizer", event)

        self.assertIn("risks", critic_prompt.lower())
        self.assertIn("trade-offs", strategist_prompt.lower())
        self.assertIn("consensus", synthesizer_prompt.lower())

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

    def test_build_reply_events_can_handoff_to_second_role(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "strategist",
            "prompt": "Evaluate the product idea",
            "topic": "Claw95",
        }
        events = build_reply_events(
            name="strategist",
            event=event,
            provider="deterministic",
            next_role="critic",
        )
        self.assertIsNotNone(events)
        assert events is not None
        self.assertEqual(len(events), 2)
        self.assertIn("Strategist", events[0]["content"])
        self.assertEqual(events[1]["type"], "handoff.submit")
        self.assertEqual(events[1]["role"], "critic")
        self.assertIn("Strategist", events[1]["prompt"])

    def test_build_reply_events_uses_generation_callable_for_ollama_mode(self) -> None:
        event = {
            "type": "room.role_prompt",
            "role": "critic",
            "prompt": "Review this launch plan",
            "topic": "Launch review",
        }

        def fake_generate(role: str, prompt: str, provider: str, model: str | None) -> str:
            self.assertEqual(role, "critic")
            self.assertEqual(provider, "ollama")
            self.assertEqual(model, "llama3.2:latest")
            self.assertIn("Launch review", prompt)
            return "Critic: local model reply"

        events = build_reply_events(
            name="critic",
            event=event,
            provider="ollama",
            model="llama3.2:latest",
            generate_reply=fake_generate,
        )
        self.assertIsNotNone(events)
        assert events is not None
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["content"], "Critic: local model reply")

    def test_should_respond_when_max_turns_is_none(self) -> None:
        self.assertTrue(should_respond(turn_count=999, max_turns=None))

    def test_should_respond_with_turn_budget(self) -> None:
        self.assertTrue(should_respond(turn_count=0, max_turns=2))
        self.assertTrue(should_respond(turn_count=1, max_turns=2))
        self.assertFalse(should_respond(turn_count=2, max_turns=2))


if __name__ == "__main__":
    unittest.main()
