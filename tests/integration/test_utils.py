import os

from src.cs_whatsapp_bot import utils


def test_make_headers_from_env():
    token = os.getenv("WHATSAPP_ACCESS_TOKEN", "test_token")
    headers = utils.make_headers_from_env()
    assert headers.get("Authorization", "").endswith(token)
