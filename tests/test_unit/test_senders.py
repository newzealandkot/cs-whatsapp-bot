from src.cs_whatsapp_bot import MESSAGE, FakeMessageSender


def test_message_sender():
    sender = FakeMessageSender()
    total_messages = sender.total_messages
    total_messages_after = total_messages + 1
    sender.send(MESSAGE)
    assert sender.total_messages == total_messages_after
