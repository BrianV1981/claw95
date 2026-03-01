from src.events import validate_inbound_event


def test_validate_join_requires_sender_id() -> None:
    ok, err = validate_inbound_event({"type": "join", "sender": {"id": "a"}})
    assert ok and err is None

    ok, err = validate_inbound_event({"type": "join", "sender": {}})
    assert not ok and err


def test_validate_message_submit() -> None:
    ok, err = validate_inbound_event({"type": "message.submit", "content": "hi"})
    assert ok and err is None

    ok, err = validate_inbound_event({"type": "message.submit", "content": 123})
    assert not ok and err
