import pytest
import pytest_httpserver as server
from fastapi import status, testclient

from src.cs_whatsapp_bot import app, bot, get_bot, repositories, senders


LOCALHOST_URL = "http://localhost:8000"
REPLY_URL = LOCALHOST_URL + "/reply"


@pytest.fixture
def client():
    with testclient.TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def get_test_bot():
    repo = repositories.FakeRepository()
    sender = senders.HTTPX2Sender("localhost", 4000)
    return bot.Bot(repository=repo, sender=sender)


@pytest.mark.anyio
async def test_reply_endpoint_sends_post_to_remote_server(
        client,
        env_token,
        request_options,
        test_server,
        webhook_payload,
):
    app.dependency_overrides[get_bot] = get_test_bot
    client.post(REPLY_URL, json=webhook_payload)
    test_server.assert_request_made(server.RequestMatcher(**request_options))


def test_reply_endpoint_rejects_invalid_payload_request(client, bad_payload):
        response = client.post(REPLY_URL, json=bad_payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_endpoint_sends_only_one_message_per_unknown_contact(
        client,
        sqlite_session,
        test_server,
        webhook_payload,
    ):
    repo = repositories.SQLiteRepository(sqlite_session)
    sender = senders.HTTPX2Sender("localhost", 4000)
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    client.post(REPLY_URL, json=webhook_payload)
    client.post(REPLY_URL, json=webhook_payload)
    assert len(test_server.log) == 1
