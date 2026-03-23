import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from src.replay import emit_summary, load_events


class ReplayTests(unittest.TestCase):
    def test_load_events_reads_jsonl_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"event_type": "join", "sender_id": "human"}),
                        json.dumps({"event_type": "message_published", "sender_id": "critic"}),
                    ]
                ),
                encoding="utf-8",
            )

            rows = load_events(path)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["event_type"], "join")

    def test_load_events_filters_by_event_type(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "events.jsonl"
            path.write_text(
                "\n".join(
                    [
                        json.dumps({"event_type": "join", "sender_id": "human"}),
                        json.dumps({"event_type": "message_published", "sender_id": "critic"}),
                    ]
                ),
                encoding="utf-8",
            )

            rows = load_events(path, event_type="message_published")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["sender_id"], "critic")

    def test_emit_summary_prints_readable_lines(self) -> None:
        events = [
            {"event_type": "join", "sender_id": "human", "ts": "2026-03-23T10:00:00Z"},
            {"event_type": "room_command", "sender_id": "human", "command": "pause", "ts": "2026-03-23T10:00:01Z"},
        ]

        output = io.StringIO()
        with redirect_stdout(output):
            emit_summary(events)

        text = output.getvalue()
        self.assertIn("join", text)
        self.assertIn("room_command", text)
        self.assertIn("pause", text)


if __name__ == "__main__":
    unittest.main()
