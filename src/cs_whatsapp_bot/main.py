import whatsapp_cloud_api


class Bot:

    async def answer(self, message: str) -> Response:
        return Response('I am bot')


class Response:

    def __init__(self, text: str) -> None:
        self.text = text


