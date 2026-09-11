import pytest

from src.cs_whatsapp_bot import Bot, FakeMessageSender, FakeRepository, FORM


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
