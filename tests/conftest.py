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


@pytest.fixture(params=[
    {},
    {"invalid_field": "string"},
])
def bad_payload(request):
    return request.param


@pytest.fixture
def profile_payload():
    return {"name": "some_name"}


@pytest.fixture
def contact_payload(profile_payload):
    return {
        "profile": profile_payload,
        "wa_id": "whatsapp_id",
    }


@pytest.fixture
def metadata_payload():
    return {
        "display_phone_number": "phone_number",
        "phone_number_id": "number_id",
    }


@pytest.fixture
def text_payload():
    return {"body": "message"}


@pytest.fixture
def message_payload(text_payload):
    return {
        "from": "phone_number",
        "id": "whatsapp_message_id",
        "timestamp": "seconds",
        "text": text_payload,
        "type": "text",
    }


@pytest.fixture
def value_payload(contact_payload, message_payload, metadata_payload):
    return {
        "messaging_product": "whatsapp",
        "metadata": metadata_payload,
        "contacts": [contact_payload],
        "messages": [message_payload],
    }


@pytest.fixture
def change_payload(value_payload):
    return {
        "field": "messages",
        "value": value_payload,
    }


@pytest.fixture
def entry_payload(change_payload):
    return {
        "id": "your_waba_id",
        "changes": [change_payload],
    }


@pytest.fixture
def webhook_payload(entry_payload):
    return {
        "object": "whatsapp_business_account",
        "entry": [entry_payload],
    }
