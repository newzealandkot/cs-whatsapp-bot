from src.cs_whatsapp_bot import FORM, WhatsAppWebhookEvent, utils


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


def test_extract_message_id_from_event(webhook_event):
    message_id = utils.extract_message_id_from_event(webhook_event)
    assert message_id == "whatsapp_message_id"


def test_extract_message_id_from_event_returns_none_for_status_only_event(status_only_webhook_payload):
    event = WhatsAppWebhookEvent.model_validate(status_only_webhook_payload)
    message_id = utils.extract_message_id_from_event(event)
    assert message_id is None


def test_build_output_payload(expected_payload, recipient):
    payload = utils.build_output_payload(contact=recipient, body=FORM)
    assert payload == expected_payload


# def test_build_payload_from_event(expected_payload, webhook_payload):
#     event = WhatsAppWebhookEvent.model_validate(webhook_payload)
#     payload = utils.build_payload_from_event(event)
#     assert payload == expected_payload
