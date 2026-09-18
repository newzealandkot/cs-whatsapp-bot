from src.cs_whatsapp_bot import FORM, utils, WhatsAppWebhookEvent


def test_extract_contact_from_event(recipient, webhook_event):
    contact = utils.extract_contact_from_event(webhook_event)
    assert contact == recipient


def test_extract_contact_from_event_returns_none_for_status_only_event(status_only_webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(status_only_webhook_payload)
    contact = utils.extract_contact_from_event(event)
    assert contact is None


def test_extract_contact_from_event_returns_none_for_non_text_message(image_only_webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(image_only_webhook_payload)
    contact = utils.extract_contact_from_event(event)
    assert contact is None


def test_build_output_payload(expected_payload, recipient):
    payload = utils.build_output_payload(contact=recipient, body=FORM)
    assert payload == expected_payload


def test_get_headers_from_env(expected_headers, env_token):
    headers = utils.make_headers_from_env()
    assert headers == expected_headers


# def test_build_payload_from_event(expected_payload, webhook_payload):
#     event = WhatsAppWebhookEvent.model_validate(webhook_payload)
#     payload = utils.build_payload_from_event(event)
#     assert payload == expected_payload
