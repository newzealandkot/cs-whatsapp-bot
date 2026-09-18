import pytest

from src.cs_whatsapp_bot import (
    FORM,
    Bot,
    FakeMessageSender,
    FakeRepository,
    WhatsAppWebhookEvent,
)


def test_bot_has_message():
    assert Bot.FORM == FORM


@pytest.mark.anyio
async def test_bot_sends_message_for_new_contact(webhook_event):
    repo = FakeRepository()
    sender = FakeMessageSender()
    bot = Bot(repo, sender)
    await bot.send_message(webhook_event)
    assert sender.total_messages == 1


@pytest.mark.anyio
async def test_no_message_from_bot_for_known_contact(recipient, webhook_event):
    repo = FakeRepository()
    repo.add(recipient)
    sender = FakeMessageSender()
    bot = Bot(repo, sender)
    await bot.send_message(webhook_event)
    assert sender.total_messages == 0


@pytest.mark.anyio
async def test_bot_sends_message_only_once_even_if_same_contact_writes_again(webhook_event):
    repo = FakeRepository()
    sender = FakeMessageSender()
    bot = Bot(repo, sender)
    await bot.send_message(webhook_event)
    await bot.send_message(webhook_event)
    assert sender.total_messages == 1


@pytest.mark.anyio
async def test_bot_does_nothing_for_status_only_event(status_only_webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(status_only_webhook_payload)
    repo = FakeRepository()
    sender = FakeMessageSender()
    bot = Bot(repo, sender)
    await bot.send_message(event)
    assert sender.total_messages == 0


@pytest.mark.anyio
async def test_bot_does_not_send_form_for_non_text_message(image_only_webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(image_only_webhook_payload)
    repo = FakeRepository()
    sender = FakeMessageSender()
    bot = Bot(repo, sender)
    await bot.send_message(event)
    assert sender.total_messages == 0


@pytest.mark.anyio
async def test_bot_sends_nothing_for_two_different_message_ids_from_known_contact(recipient, webhook_payload):
    repo = FakeRepository()
    repo.add(recipient)
    sender = FakeMessageSender()
    bot = Bot(repo, sender)

    first_event = WhatsAppWebhookEvent.model_validate(webhook_payload)
    await bot.send_message(first_event)

    webhook_payload["entry"][0]["changes"][0]["value"]["messages"][0]["id"] = "a_different_message_id"
    second_event = WhatsAppWebhookEvent.model_validate(webhook_payload)
    await bot.send_message(second_event)

    assert sender.total_messages == 0


@pytest.mark.anyio
async def test_bot_releases_claim_and_allows_retry_when_send_fails(webhook_event):
    repo = FakeRepository()
    sender = FakeMessageSender(should_fail=True)
    bot = Bot(repo, sender)

    with pytest.raises(RuntimeError):
        await bot.send_message(webhook_event)
    assert sender.total_messages == 0

    sender.should_fail = False
    await bot.send_message(webhook_event)
    assert sender.total_messages == 1


class _RepositoryThatFailsToAddContact(FakeRepository):

    def add(self, user):
        raise RuntimeError("simulated repo.add failure")


@pytest.mark.anyio
async def test_bot_keeps_claim_when_repo_add_fails_after_successful_send(webhook_event):
    repo = _RepositoryThatFailsToAddContact()
    sender = FakeMessageSender()
    bot = Bot(repo, sender)

    with pytest.raises(RuntimeError):
        await bot.send_message(webhook_event)
    assert sender.total_messages == 1

    await bot.send_message(webhook_event)
    assert sender.total_messages == 1


# @pytest.fixture
# def bot():
#     return Bot()
#
#
# def test_can_start_bot(bot):
#     bot.is_active = False
#     bot.start()
#     assert bot.is_active
#
#
# def test_can_stop_bot(bot):
#     bot.is_active = True
#     bot.stop()
#     assert not bot.is_active
#
#
# def test_bot_can_return_message(bot):
#     bot.start()
#     message = bot.message()
#     assert message == MESSAGE
#
#
# def test_can_message_only_active_bot(bot):
#     bot.is_active = False
#     exc_message = "Bot is inactive, call 'start' method to activate bot"
#     with pytest.raises(BotInactiveError, match=exc_message):
#         bot.message()
