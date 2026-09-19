import pytest

from src.cs_whatsapp_bot import FORM, FakeMessageSender, HTTPX2Sender


@pytest.mark.anyio
async def test_message_sender():
    sender = FakeMessageSender()
    total_messages = sender.total_messages
    total_messages_after = total_messages + 1
    await sender.send(FORM)
    assert sender.total_messages == total_messages_after


def test_httpx2sender_builds_default_base_url_from_api_version():
    sender = HTTPX2Sender(phone_number_id="123", access_token="token", api_version="v26.0")
    assert sender.base_url == "https://graph.facebook.com/v26.0"


def test_httpx2sender_uses_explicit_base_url_override():
    sender = HTTPX2Sender(phone_number_id="123", access_token="token", base_url="http://localhost:9999")
    assert sender.base_url == "http://localhost:9999"


def test_httpx2sender_defaults_api_version():
    sender = HTTPX2Sender(phone_number_id="123", access_token="token")
    assert sender.base_url == "https://graph.facebook.com/v26.0"
