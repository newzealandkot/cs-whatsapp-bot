from . import schemas
from . import utils


FORM = "Please fill out this form:"


class Bot:
    FORM = FORM

    def __init__(self, repository, sender):
        self.repo = repository
        self.sender = sender

    async def send_message(self, event: schemas.WhatsAppWebhookEvent):
        contact = utils.extract_contact_from_event(event)
        if self.repo.get(contact) is None:
            payload = utils.build_output_payload(body=self.FORM, contact=contact)
            await self.sender.send(payload)
