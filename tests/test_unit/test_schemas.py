import pydantic as pd
import pytest

from src.cs_whatsapp_bot import Contact, Message, Metadata, Profile, Text


@pytest.fixture(params=[
    Contact,
    Metadata,
    Message,
    Profile,
    Text,
])
def schema(request):
    return request.param


@pytest.fixture(params=[
    {},
    {"invalid_field": "string"},
])
def bad_payload(request):
    return request.param


@pytest.fixture
def profile_payload():
    return {"name": "some_name"}


@pytest.fixture
def contact_payload(profile_payload):
    return {
        "profile": profile_payload,
        "wa_id": "whatsapp_id",
    }


@pytest.fixture
def metadata_payload():
    return {
        "display_phone_number": "phone_number",
        "phone_number_id": "number_id",
    }


@pytest.fixture
def text_payload():
    return {"body": "message"}


@pytest.fixture
def message_payload(text_payload):
    return {
        "from": "phone_number",
        "id": "whatsapp_message_id",
        "timestamp": "seconds",
        "text": text_payload,
        "type": "text",
    }


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


def test_schema_rejects_invalid_payload(bad_payload, schema):
    with pytest.raises(pd.ValidationError):
        schema.model_validate(bad_payload)


# def test_value_parses_valid_payload():
#     payload = {
#         "messaging_product": "whatsapp",
#         "metadata": {
#             "display_phone_number": "15550000000",
#             "phone_number_id": "YOUR_PHONE_NUMBER_ID"
#         },
#         "contacts": [
#             {
#                 "profile": {
#                     "name": "John"
#                 },
#                 "wa_id": "77001234567"
#             }
#         ],
#         "messages": [
#             {
#                 "from": "77001234567",
#                 "id": "wamid.HBgL...",
#                 "timestamp": "1720000000",
#                 "text": {
#                     "body": "Привет!"
#                 },
#                 "type": "text"
#             }
#         ]
#     }



