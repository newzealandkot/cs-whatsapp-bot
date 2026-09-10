import pytest
import pytest_httpserver as server
from fastapi import status, testclient

from src.cs_whatsapp_bot import app


LOCALHOST_URL = "http://localhost:8000"
REPLY_URL = LOCALHOST_URL + "/reply"

client = testclient.TestClient(app)


@pytest.mark.anyio
async def test_reply_endpoint_sends_post_to_remote_server(
        env_token,
        request_options,
        test_server,
        webhook_payload,
):
    client.post(REPLY_URL, json=webhook_payload)
    test_server.assert_request_made(server.RequestMatcher(**request_options))


def test_reply_endpoint_rejects_invalid_payload_request(bad_payload):
    response = client.post(
        REPLY_URL,
        json=bad_payload,
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
