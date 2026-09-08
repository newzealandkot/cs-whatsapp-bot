from src.cs_whatsapp_bot import utils


def test_make_whatsapp_message_payload():
    expected_payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "0123456789",
        "type": "text",
        "text": {
            "preview_url": False,
            "body": "Здравствуйте! Заполните пожалуйста анкету:"
        },
    }
    recipient = "0123456789"
    body = "Здравствуйте! Заполните пожалуйста анкету:"
    payload = utils.make_whatsapp_message_payload(recipient, body)
    assert payload == expected_payload
