from .utils import make_whatsapp_message_payload


FORM = "Please fill out this form:"


class Bot:
    FORM = FORM

    def __init__(self, sender):
        self.sender = sender

    async def send_message(self, recipient):
        payload = make_whatsapp_message_payload(body=self.FORM, recipient=recipient)
        await self.sender.send(payload)
