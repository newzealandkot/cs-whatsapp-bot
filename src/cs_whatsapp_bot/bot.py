from . import schemas
from . import utils


FORM = "Please fill out this form:"


class Bot:
    FORM = FORM

    def __init__(self, sender):
        self.sender = sender

    async def send_message(self, event: schemas.WhatsAppWebhookEvent):
        payload = utils.build_payload_from_event(body=self.FORM, event=event)
        await self.sender.send(payload)
