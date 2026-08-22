import pytest

from src.cs_whatsapp_bot.main import Bot


def test_whatsapp_cloud_api_is_installed() -> None:
    try:
        import whatsapp_cloud_api
    except ModuleNotFoundError:
        assert False
    assert whatsapp_cloud_api is not None

@pytest.mark.anyio
async def test_async() -> None:
    assert True

@pytest.mark.anyio
async def test_greeting() -> None:
    bot = Bot()
    response = await bot.answer('Hello')
    assert response.text == ('I am bot')
