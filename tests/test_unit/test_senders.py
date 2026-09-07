import pytest

from src.cs_whatsapp_bot import MESSAGE, FakeMessageSender


@pytest.mark.anyio
async def test_message_sender():
    sender = FakeMessageSender()
    total_messages = sender.total_messages
    total_messages_after = total_messages + 1
    await sender.send(MESSAGE)
    assert sender.total_messages == total_messages_after
