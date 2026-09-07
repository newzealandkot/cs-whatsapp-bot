import pytest
from fastapi import testclient

from src.cs_whatsapp_bot import app


LOCALHOST_URL = "http://localhost:8000"
REPLY_URL = LOCALHOST_URL + "/reply"

client = testclient.TestClient(app)


@pytest.mark.anyio
async def test_reply_endpoint_sends_post_to_remote_server(test_server):
    client.post(REPLY_URL)
