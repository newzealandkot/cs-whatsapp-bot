from http import HTTPMethod

import pytest

from src.cs_whatsapp_bot import FORM


HTTPSERVER_HOST_PORT = ("localhost", 4000)


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return HTTPSERVER_HOST_PORT


@pytest.fixture
def remote_uri():
    return "/remote"


@pytest.fixture
def recipient():
    return "0123456789"


@pytest.fixture
def expected_payload(recipient):
    expected_payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": FORM,
        },
    }
    return expected_payload


@pytest.fixture
def request_options(expected_payload, remote_uri):
    request_options = {
        "uri": remote_uri,
        "method": HTTPMethod.POST,
        "json": expected_payload,
    }
    return request_options


@pytest.fixture
def test_server(httpserver, request_options):
    httpserver.expect_request(**request_options).respond_with_json({})
    return httpserver
