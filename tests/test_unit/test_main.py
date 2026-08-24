from src.cs_whatsapp_bot.main import Bot

def test_start_activates_bot():
    bot = Bot()
    bot.start()
    assert bot.is_active
