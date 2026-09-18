import pytest
import pytest_httpserver as server

from src.cs_whatsapp_bot import Bot, HTTPX2Sender, SQLiteRepository


@pytest.mark.anyio
async def test_bot_can_send_message_to_remote_server(
        env_token,
        webhook_event,
        request_options,
        sqlite_session,
        test_server,
):
    repo = SQLiteRepository(sqlite_session)
    sender = HTTPX2Sender(host=test_server.host, port=test_server.port)
    bot = Bot(repo, sender)
    await bot.send_message(webhook_event)
    test_server.assert_request_made(server.RequestMatcher(**request_options))
