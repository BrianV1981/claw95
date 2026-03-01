from pathlib import Path

from src.sinks import JsonlSink, MarkdownSink, build_sinks


def test_build_sinks_local_outputs(tmp_path: Path) -> None:
    cfg = {
        "sinks": {
            "jsonl_enabled": True,
            "jsonl_path": str(tmp_path / "mirror.jsonl"),
            "markdown_enabled": True,
            "markdown_path": str(tmp_path / "transcript.md"),
            "discord_webhook_url": "",
        }
    }
    sinks = build_sinks(cfg)
    assert len(sinks) == 2


def test_markdown_sink_writes_messages(tmp_path: Path) -> None:
    sink = MarkdownSink(tmp_path / "t.md")
    sink.publish(
        {
            "type": "message.published",
            "sender": {"id": "a"},
            "content": "hello",
            "ts": "now",
        }
    )
    txt = (tmp_path / "t.md").read_text(encoding="utf-8")
    assert "hello" in txt


def test_jsonl_sink_writes_rows(tmp_path: Path) -> None:
    sink = JsonlSink(tmp_path / "m.jsonl")
    sink.publish({"type": "x"})
    txt = (tmp_path / "m.jsonl").read_text(encoding="utf-8")
    assert '"type": "x"' in txt
