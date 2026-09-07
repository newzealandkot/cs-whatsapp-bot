import pytest

from src.cs_whatsapp_bot import Bot, HTTPX2Sender


@pytest.mark.anyio
async def test_bot_can_send_message_to_remote_server_2(test_server):
    sender = HTTPX2Sender(*test_server)
    bot = Bot(sender)
    await bot.send_message()
