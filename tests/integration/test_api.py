import hashlib
import hmac
import json

import pytest
import pytest_httpserver as server
from fastapi import status, testclient

from src.cs_whatsapp_bot import app, bot, get_bot, repositories, senders


LOCALHOST_URL = "http://localhost:8000"
WEBHOOK_URL = LOCALHOST_URL + "/webhook"


@pytest.fixture
def client():
    with testclient.TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def get_test_bot():
    repo = repositories.FakeRepository()
    sender = senders.HTTPX2Sender("localhost", 4000)
    return bot.Bot(repository=repo, sender=sender)


def post_signed(client, url, payload, secret):
    body = json.dumps(payload).encode()
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": f"sha256={digest}",
    }
    return client.post(url, content=body, headers=headers)


@pytest.mark.anyio
async def test_webhook_endpoint_accepts_valid_signature_and_behaves_as_before(
        client,
        app_secret,
        env_token,
        request_options,
        test_server,
        webhook_payload,
):
    app.dependency_overrides[get_bot] = get_test_bot
    response = post_signed(client, WEBHOOK_URL, webhook_payload, app_secret)
    assert response.status_code == status.HTTP_200_OK
    test_server.assert_request_made(server.RequestMatcher(**request_options))


def test_webhook_endpoint_rejects_invalid_payload_request(client, app_secret, bad_payload):
    response = post_signed(client, WEBHOOK_URL, bad_payload, app_secret)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_endpoint_sends_only_one_message_per_unknown_contact(
        client,
        app_secret,
        sqlite_session,
        test_server,
        webhook_payload,
    ):
    repo = repositories.SQLiteRepository(sqlite_session)
    sender = senders.HTTPX2Sender("localhost", 4000)
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    post_signed(client, WEBHOOK_URL, webhook_payload, app_secret)
    post_signed(client, WEBHOOK_URL, webhook_payload, app_secret)
    assert len(test_server.log) == 1


def test_webhook_verification_returns_challenge_for_correct_token(client, monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")
    response = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "test_verify_token",
        "hub.challenge": "12345",
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.text == "12345"


def test_webhook_verification_rejects_wrong_token(client, monkeypatch):
    monkeypatch.setenv("WHATSAPP_VERIFY_TOKEN", "test_verify_token")
    response = client.get("/webhook", params={
        "hub.mode": "subscribe",
        "hub.verify_token": "wrong_token",
        "hub.challenge": "12345",
    })
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_webhook_endpoint_rejects_wrong_signature(client, app_secret, webhook_payload):
    repo = repositories.FakeRepository()
    sender = senders.FakeMessageSender()
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    body = json.dumps(webhook_payload).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "sha256=" + "a" * 64,
    }
    response = client.post(WEBHOOK_URL, content=body, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert sender.total_messages == 0


def test_webhook_endpoint_rejects_missing_signature_header(client, app_secret, webhook_payload):
    repo = repositories.FakeRepository()
    sender = senders.FakeMessageSender()
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    body = json.dumps(webhook_payload).encode()
    response = client.post(WEBHOOK_URL, content=body, headers={"Content-Type": "application/json"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert sender.total_messages == 0


def test_webhook_endpoint_rejects_malformed_signature_header(client, app_secret, webhook_payload):
    repo = repositories.FakeRepository()
    sender = senders.FakeMessageSender()
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    body = json.dumps(webhook_payload).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": "not-a-valid-signature",
    }
    response = client.post(WEBHOOK_URL, content=body, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert sender.total_messages == 0


def test_webhook_endpoint_rejects_when_body_tampered_after_signing(client, app_secret, webhook_payload):
    repo = repositories.FakeRepository()
    sender = senders.FakeMessageSender()
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    original_body = json.dumps(webhook_payload).encode()
    digest = hmac.new(app_secret.encode(), original_body, hashlib.sha256).hexdigest()
    tampered_body = json.dumps({**webhook_payload, "object": "tampered"}).encode()
    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": f"sha256={digest}",
    }
    response = client.post(WEBHOOK_URL, content=tampered_body, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert sender.total_messages == 0


def test_webhook_endpoint_rejects_invalid_json_with_bad_signature_without_processing(client, app_secret):
    repo = repositories.FakeRepository()
    sender = senders.FakeMessageSender()
    app.dependency_overrides[get_bot] = lambda: bot.Bot(repository=repo, sender=sender)
    response = client.post(
        WEBHOOK_URL,
        content=b"{not json",
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": "sha256=" + "a" * 64,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert sender.total_messages == 0
