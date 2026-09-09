import httpx2

from .import utils


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
        url = f"http://{self.host}:{self.port}/remote"    # hardcode
        headers = utils.make_headers_from_env()
        async with httpx2.AsyncClient() as client:
            await client.post(url, json=payload, headers=headers)
        self.total_messages += 1
