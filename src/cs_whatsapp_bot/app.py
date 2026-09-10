import fastapi

from . import bot
from . import schemas
from . import senders


app = fastapi.FastAPI()


@app.post("/reply")
async def reply(event: schemas.WhatsAppWebhookEvent):
    sender = senders.HTTPX2Sender("localhost", 4000) # hardcode
    whatsapp_bot = bot.Bot(sender)
    await whatsapp_bot.send_message(event)


#
# if __name__ == "__main__":
#     uvicorn.run(app)
