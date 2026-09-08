import pytest
import pytest_httpserver as server

from src.cs_whatsapp_bot import HTTPX2Sender


@pytest.mark.anyio
async def test_sender_sends_message_to_remote_server(env_token, expected_payload, request_options, test_server):
    sender = HTTPX2Sender(host=test_server.host, port=test_server.port)
    await sender.send(expected_payload)
    test_server.assert_request_made(server.RequestMatcher(**request_options))
