import pytest

from src.cs_whatsapp_bot import HTTPX2Sender, MESSAGE


@pytest.mark.anyio
async def test_sender_sends_message_to_remote_server(test_server):
    sender = HTTPX2Sender(*test_server)
    await sender.send(MESSAGE)
