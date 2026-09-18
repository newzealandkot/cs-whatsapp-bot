import pydantic as pd
import pytest

from src.cs_whatsapp_bot import (
    Change,
    Contact,
    Entry,
    Message,
    Metadata,
    Profile,
    Text,
    Value,
    WhatsAppWebhookEvent,
)


@pytest.fixture(params=[
    Change,
    Contact,
    Entry,
    Metadata,
    Message,
    Profile,
    Text,
    Value,
    WhatsAppWebhookEvent,
])
def schema(request):
    return request.param


def test_profile_parses_valid_payload(profile_payload):
    profile = Profile.model_validate(profile_payload)
    assert profile.model_dump() == profile_payload


def test_contact_parses_valid_payload(contact_payload):
    contact = Contact.model_validate(contact_payload)
    assert contact.model_dump() == contact_payload


def test_metadata_parses_valid_payload(metadata_payload):
    metadata = Metadata.model_validate(metadata_payload)
    assert metadata.model_dump() == metadata_payload


def test_text_parses_valid_payload(text_payload):
    text = Text.model_validate(text_payload)
    assert text.model_dump() == text_payload


def test_message_parses_valid_payload(message_payload):
    message = Message.model_validate(message_payload)
    assert message.model_dump(by_alias=True) == message_payload


def test_message_parses_from_alias(message_payload):
    message = Message.model_validate(message_payload)
    assert message.from_ == "phone_number"


def test_value_parses_valid_payload(value_payload):
    value = Value.model_validate(value_payload)
    assert value.model_dump(by_alias=True) == value_payload


def test_change_parses_valid_payload(change_payload):
    change = Change.model_validate(change_payload)
    assert change.model_dump(by_alias=True) == change_payload


def test_entry_parses_valid_payload(entry_payload):
    entry = Entry.model_validate(entry_payload)
    assert entry.model_dump(by_alias=True) == entry_payload


def test_whatsapp_webhook_event_parses_valid_payload(webhook_payload):
    whatsapp_webhook_event = WhatsAppWebhookEvent.model_validate(webhook_payload)
    assert whatsapp_webhook_event.model_dump(by_alias=True) == webhook_payload


def test_value_parses_status_only_payload(status_only_value_payload):
    value = Value.model_validate(status_only_value_payload)
    assert value.messages == []
    assert value.contacts == []


def test_message_parses_image_message_without_text(image_message_payload):
    message = Message.model_validate(image_message_payload)
    assert message.text is None
    assert message.type == "image"


def test_schema_rejects_invalid_payload(bad_payload, schema):
    with pytest.raises(pd.ValidationError):
        schema.model_validate(bad_payload)
