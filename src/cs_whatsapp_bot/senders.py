import httpx2


class FakeMessageSender:

    def __init__(self, host="localhost", port=8000, should_fail=False):
        self.total_messages = 0
        self.should_fail = should_fail

    async def send(self, message):
        if self.should_fail:
            raise RuntimeError("FakeMessageSender configured to fail")
        self.total_messages += 1


class HTTPX2Sender:

    def __init__(self, phone_number_id: str, access_token: str, api_version: str = "v26.0", base_url: str | None = None):
        self.phone_number_id = phone_number_id
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = base_url if base_url is not None else f"https://graph.facebook.com/{api_version}"
        self.total_messages = 0

    async def send(self, payload):
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        async with httpx2.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        self.total_messages += 1
