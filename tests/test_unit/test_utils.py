from src.cs_whatsapp_bot import FORM, utils


def test_make_whatsapp_message_payload(expected_payload, recipient):
    payload = utils.make_whatsapp_message_payload(recipient=recipient, body=FORM)
    assert payload == expected_payload


def test_get_headers_from_env(expected_headers, env_token):
    headers = utils.make_headers_from_env()
    assert headers == expected_headers
