import sqlite3
from http import HTTPMethod

import pytest

from src.cs_whatsapp_bot import FORM, WhatsAppWebhookEvent

HTTPSERVER_HOST_PORT = ("localhost", 4000)
TEST_SENDER_PHONE = "phone_number"
TEST_PHONE_NUMBER_ID = "test_phone_number_id"
TEST_ACCESS_TOKEN = "test_access_token"


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return HTTPSERVER_HOST_PORT


@pytest.fixture
def sqlite_session():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    create_table_phones = """
        CREATE TABLE phones (
            id INTEGER PRIMARY KEY,
            phone TEXT NOT NULL UNIQUE
        )
        """
    conn.execute(create_table_phones)
    create_table_processed_messages = """
        CREATE TABLE processed_messages (
            message_id TEXT PRIMARY KEY
        )
        """
    conn.execute(create_table_processed_messages)
    yield conn
    conn.close()


@pytest.fixture
def sqlite_file_path(tmp_path):
    path = str(tmp_path / "test.db")
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE phones (
            id INTEGER PRIMARY KEY,
            phone TEXT NOT NULL UNIQUE
        )
        """)
    conn.execute("""
        CREATE TABLE processed_messages (
            message_id TEXT PRIMARY KEY
        )
        """)
    conn.commit()
    conn.close()
    return path


@pytest.fixture
def app_secret(monkeypatch):
    monkeypatch.setenv("WHATSAPP_APP_SECRET", "test_app_secret")
    return "test_app_secret"


@pytest.fixture
def phone_number_id():
    return TEST_PHONE_NUMBER_ID


@pytest.fixture
def access_token():
    return TEST_ACCESS_TOKEN


@pytest.fixture
def remote_uri(phone_number_id):
    return f"/{phone_number_id}/messages"


@pytest.fixture
def recipient():
    return TEST_SENDER_PHONE


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
def expected_headers(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
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
    httpserver.expect_request(**request_options).respond_with_data("OK")
    return httpserver


@pytest.fixture
def base_url(test_server):
    return f"http://{test_server.host}:{test_server.port}"


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
def message_payload(recipient, text_payload):
    return {
        "from": recipient,
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
        "statuses": [],
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

@pytest.fixture
def webhook_event(webhook_payload):
    return WhatsAppWebhookEvent.model_validate(webhook_payload)


@pytest.fixture
def status_payload():
    return {
        "id": "wamid.status_id",
        "status": "delivered",
        "timestamp": "seconds",
        "recipient_id": TEST_SENDER_PHONE,
    }


@pytest.fixture
def status_only_value_payload(metadata_payload, status_payload):
    return {
        "messaging_product": "whatsapp",
        "metadata": metadata_payload,
        "statuses": [status_payload],
    }


@pytest.fixture
def status_only_webhook_payload(status_only_value_payload):
    return {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "your_waba_id",
            "changes": [{
                "field": "messages",
                "value": status_only_value_payload,
            }],
        }],
    }


@pytest.fixture
def image_message_payload(recipient):
    return {
        "from": recipient,
        "id": "whatsapp_message_id",
        "timestamp": "seconds",
        "type": "image",
        "image": {
            "id": "media-id",
            "mime_type": "image/jpeg",
            "sha256": "hash",
        },
    }


@pytest.fixture
def image_only_value_payload(contact_payload, image_message_payload, metadata_payload):
    return {
        "messaging_product": "whatsapp",
        "metadata": metadata_payload,
        "contacts": [contact_payload],
        "messages": [image_message_payload],
    }


@pytest.fixture
def image_only_webhook_payload(image_only_value_payload):
    return {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "your_waba_id",
            "changes": [{
                "field": "messages",
                "value": image_only_value_payload,
            }],
        }],
    }
