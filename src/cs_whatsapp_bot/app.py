import fastapi

from . import bot
from . import repositories
from . import schemas
from . import senders


app = fastapi.FastAPI()


@app.post("/reply")
async def reply(event: schemas.WhatsAppWebhookEvent):
    repo = repositories.FakeRepository()
    sender = senders.HTTPX2Sender("localhost", 4000) # hardcode
    whatsapp_bot = bot.Bot(repo, sender)
    await whatsapp_bot.send_message(event)


#
# if __name__ == "__main__":
#     uvicorn.run(app)
