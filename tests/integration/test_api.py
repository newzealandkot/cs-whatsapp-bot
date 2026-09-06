import http

from fastapi import status, testclient

from src.cs_whatsapp_bot import app


LOCALHOST_URL = "http://localhost:8000"
REPLY_URL = LOCALHOST_URL + "/reply"

client = testclient.TestClient(app)


def test_reply_endpoint_post_returns_status_ok():
    response = client.post(REPLY_URL)
    assert response.status_code == status.HTTP_200_OK


def test_reply_endpoint_sends_post_to_remote_server(httpserver):
    httpserver.expect_request("/", method=http.HTTPMethod.POST)
    client.post(REPLY_URL)
    httpserver.check_assertions()
