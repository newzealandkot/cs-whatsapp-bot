import os

from src.cs_whatsapp_bot import make_headers_from_env


def test_make_headers_from_env():
    token = os.getenv("WHATSAPP_ACCESS_TOKEN", "test_token")
    headers = make_headers_from_env()
    assert headers.get("Authorization", "").endswith(token)
