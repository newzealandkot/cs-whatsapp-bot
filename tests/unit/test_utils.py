from src.cs_whatsapp_bot import FORM, utils, WhatsAppWebhookEvent


def test_build_payload_from_event(expected_payload, webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(webhook_payload)
    payload = utils.build_payload_from_event(event=event, body=FORM)
    assert payload == expected_payload


def test_get_headers_from_env(expected_headers, env_token):
    headers = utils.make_headers_from_env()
    assert headers == expected_headers


# def test_build_payload_from_event(expected_payload, webhook_payload):
#     event = WhatsAppWebhookEvent.model_validate(webhook_payload)
#     payload = utils.build_payload_from_event(event)
#     assert payload == expected_payload
