import asyncio
import copy
import sqlite3
import threading

import pytest
import pytest_httpserver as server

from src.cs_whatsapp_bot import (
    Bot,
    FakeMessageSender,
    HTTPX2Sender,
    SQLiteRepository,
    WhatsAppWebhookEvent,
)


@pytest.mark.anyio
async def test_bot_can_send_message_to_remote_server(
        env_token,
        webhook_event,
        request_options,
        sqlite_session,
        test_server,
):
    repo = SQLiteRepository(sqlite_session)
    sender = HTTPX2Sender(host=test_server.host, port=test_server.port)
    bot = Bot(repo, sender)
    await bot.send_message(webhook_event)
    test_server.assert_request_made(server.RequestMatcher(**request_options))


def test_bot_sends_message_exactly_once_for_two_concurrent_different_message_ids_of_new_contact(
        sqlite_file_path,
        webhook_payload,
):
    sender = FakeMessageSender()
    barrier = threading.Barrier(2)

    payload_a = webhook_payload
    payload_b = copy.deepcopy(webhook_payload)
    payload_b["entry"][0]["changes"][0]["value"]["messages"][0]["id"] = "message_id_b"
    event_a = WhatsAppWebhookEvent.model_validate(payload_a)
    event_b = WhatsAppWebhookEvent.model_validate(payload_b)

    def run(event):
        conn = sqlite3.connect(sqlite_file_path)
        repo = SQLiteRepository(conn)
        bot = Bot(repo, sender)
        barrier.wait()
        asyncio.run(bot.send_message(event))
        conn.close()

    threads = [
        threading.Thread(target=run, args=(event_a,)),
        threading.Thread(target=run, args=(event_b,)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert sender.total_messages == 1

    verify_conn = sqlite3.connect(sqlite_file_path)
    rows = verify_conn.execute("SELECT phone FROM phones").fetchall()
    verify_conn.close()
    assert len(rows) == 1
