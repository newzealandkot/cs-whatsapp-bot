import pytest
from src.cs_whatsapp_bot.main import Bot, BotInactiveError, MESSAGE


def test_can_start_bot():
    bot = Bot()
    bot.is_active = False
    bot.start()
    assert bot.is_active


def test_can_stop_bot():
    bot = Bot()
    bot.is_active = True
    bot.stop()
    assert not bot.is_active


def test_bot_can_return_message():
    bot = Bot()
    bot.start()
    message = bot.message()
    assert message == MESSAGE


def test_can_message_only_active_bot():
    bot = Bot()
    bot.is_active = False
    with pytest.raises(BotInactiveError):
        bot.message()
