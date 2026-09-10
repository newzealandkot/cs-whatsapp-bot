import pydantic as pd


class Profile(pd.BaseModel):
    name: str


class Contact(pd.BaseModel):
    profile: Profile
    wa_id: str


class Metadata(pd.BaseModel):
    display_phone_number: str
    phone_number_id: str


class Text(pd.BaseModel):
    body: str


class Message(pd.BaseModel):
    from_: str = pd.Field(alias="from")
    id: str
    timestamp: str
    text: Text
    type: str


class Value(pd.BaseModel):
    messaging_product: str
    metadata: Metadata
    contacts: list[Contact]
    messages: list[Message]


class Change(pd.BaseModel):
    field: str
    value: Value

class Entry(pd.BaseModel):
    id: str
    changes: list[Change]


class WhatsAppWebhookEvent(pd.BaseModel):
    object: str
    entry: list[Entry]
