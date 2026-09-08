from http import HTTPMethod

import pytest

from src.cs_whatsapp_bot import FORM


HTTPSERVER_HOST_PORT = ("localhost", 4000)


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return HTTPSERVER_HOST_PORT


@pytest.fixture
def env_token(monkeypatch):
    monkeypatch.setenv("WHATSAPP_ACCESS_TOKEN", "test_token")


@pytest.fixture
def remote_uri():
    return "/remote"


@pytest.fixture
def recipient():
    return "0123456789"


@pytest.fixture
def expected_payload(recipient):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": FORM,
        },
    }
    return payload


@pytest.fixture
def expected_headers():
    headers = {
        "Authorization": f"Bearer test_token",
        "Content-Type": "application/json",
    }
    return headers


@pytest.fixture
def request_options(expected_headers, expected_payload, remote_uri):
    request_options = {
        "uri": remote_uri,
        "method": HTTPMethod.POST,
        "json": expected_payload,
        "headers": expected_headers,
    }
    return request_options


@pytest.fixture
def test_server(httpserver, request_options):
    httpserver.expect_request(**request_options).respond_with_json({})
    return httpserver
