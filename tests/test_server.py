import json
import tempfile
import unittest
from pathlib import Path

from src.server import RoomServer


class FakeWebSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []

    async def send(self, data: str) -> None:
        self.sent.append(data)


class RoomServerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_path = str(Path(self.temp_dir.name) / "events.jsonl")
        self.server = RoomServer(log_path=self.log_path)
        self.ws = FakeWebSocket()
        self.server.clients.add(self.ws)
        self.server.usernames[self.ws] = "human"

    async def asyncTearDown(self) -> None:
        self.temp_dir.cleanup()

    async def test_pause_command_updates_room_state(self) -> None:
        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "/pause"})

        self.assertTrue(self.server.paused)
        message_types = [json.loads(message)["type"] for message in self.ws.sent]
        self.assertIn("room.command.result", message_types)
        self.assertIn("room.state", message_types)

    async def test_resume_command_unpauses_room(self) -> None:
        self.server.paused = True

        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "/resume"})

        self.assertFalse(self.server.paused)
        payloads = [json.loads(message) for message in self.ws.sent]
        command_result = next(item for item in payloads if item["type"] == "room.command.result")
        self.assertEqual(command_result["command"], "resume")

    async def test_topic_command_sets_topic(self) -> None:
        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "/topic Claw95 POC"})

        self.assertEqual(self.server.topic, "Claw95 POC")
        payloads = [json.loads(message) for message in self.ws.sent]
        state = next(item for item in payloads if item["type"] == "room.state")
        self.assertEqual(state["topic"], "Claw95 POC")

    async def test_paused_room_blocks_regular_messages(self) -> None:
        self.server.paused = True

        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "hello room"})

        payloads = [json.loads(message) for message in self.ws.sent]
        blocked = next(item for item in payloads if item["type"] == "message.blocked")
        self.assertEqual(blocked["decision"]["reason_codes"], ["PAUSED"])

    async def test_ask_command_sets_active_target(self) -> None:
        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "/ask strategist"})

        self.assertEqual(self.server.active_target, "strategist")
        payloads = [json.loads(message) for message in self.ws.sent]
        state = next(item for item in payloads if item["type"] == "room.state")
        self.assertEqual(state["active_target"], "strategist")

    async def test_ask_command_rejects_unknown_agent(self) -> None:
        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "/ask unknown"})

        payloads = [json.loads(message) for message in self.ws.sent]
        error = next(item for item in payloads if item["type"] == "error")
        self.assertEqual(error["code"], "UNKNOWN_AGENT")

    async def test_published_message_includes_active_target(self) -> None:
        self.server.active_target = "critic"

        await self.server.handle_event(self.ws, {"type": "message.submit", "content": "focus on risk"})

        payloads = [json.loads(message) for message in self.ws.sent]
        published = next(item for item in payloads if item["type"] == "message.published")
        self.assertEqual(published["target"], "critic")


if __name__ == "__main__":
    unittest.main()
