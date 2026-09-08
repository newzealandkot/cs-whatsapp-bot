from src.cs_whatsapp_bot import FORM, utils


def test_make_whatsapp_message_payload(expected_payload, recipient):
    payload = utils.make_whatsapp_message_payload(recipient=recipient, body=FORM)
    assert payload == expected_payload
