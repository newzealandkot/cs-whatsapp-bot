from . import schemas, utils

FORM = """Climatservice:

Dobar dan. Servisiramo auto i kućne klima uređaje.
1. Koja usluga vas konkretno zanima?
2. U kom gradu se nalazite?

Здравствуйте. Мы обслуживаем автомобильные и домашние кондиционеры.
1. Какая именно услуга вас интересует?
2. В каком городе вы находитесь?

Hello. We service car and home air conditioners.
1. Which specific service are you interested in?
2. Which city are you located in?"""


class Bot:
    FORM = FORM

    def __init__(self, repository, sender):
        self.repo = repository
        self.sender = sender

    async def send_message(self, event: schemas.WhatsAppWebhookEvent):
        message_id = utils.extract_message_id_from_event(event)
        if message_id is not None and not self.repo.try_claim_message(message_id):
            return
        contact = utils.extract_contact_from_event(event)
        if contact is None:
            return
        if self.repo.get(contact) is None:
            payload = utils.build_output_payload(body=self.FORM, contact=contact)
            try:
                await self.sender.send(payload)
            except Exception:
                if message_id is not None:
                    self.repo.release_message_claim(message_id)
                raise
            self.repo.add(contact)
