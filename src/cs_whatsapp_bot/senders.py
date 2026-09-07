import httpx2


class FakeMessageSender:

    def __init__(self, host="localhost", port=8000):
        self.total_messages = 0

    async def send(self, message):
        self.total_messages += 1


class HTTPX2Sender:

    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.total_messages = 0

    async def send(self, payload):
        url = f"http://{self.host}:{self.port}/remote"
        async with httpx2.AsyncClient() as client:
            await client.post(url)
        self.total_messages += 1
