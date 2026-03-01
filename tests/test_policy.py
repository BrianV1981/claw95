from pathlib import Path

from src.policy import load_policy


def test_load_policy_defaults_when_missing(tmp_path: Path) -> None:
    p = load_policy(tmp_path / "missing.yaml")
    assert p.command_prefix == "/"
    assert p.per_sender_per_min > 0


def test_load_policy_reads_file(tmp_path: Path) -> None:
    file = tmp_path / "policy.yaml"
    file.write_text(
        """
policy_version: "x"
rate_limit:
  per_sender_per_min: 7
cooldown_seconds: 0.5
duplicate_window: 4
max_message_len: 90
blocked_patterns: ["abc"]
room:
  command_prefix: "!"
  start_paused: true
""",
        encoding="utf-8",
    )

    p = load_policy(file)
    assert p.policy_version == "x"
    assert p.per_sender_per_min == 7
    assert p.command_prefix == "!"
    assert p.start_paused is True
