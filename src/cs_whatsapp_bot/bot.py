MESSAGE = "Welcome to Climate Service!"


class Bot:
    message = MESSAGE

    def __init__(self, sender):
        self.sender = sender

    async def send_message(self):
        await self.sender.send(self.message)
