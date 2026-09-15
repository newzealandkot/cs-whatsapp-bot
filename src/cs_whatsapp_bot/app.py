import os
import sqlite3
from contextlib import asynccontextmanager

import dotenv
import fastapi

from . import bot, repositories, schemas, senders, utils


dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    db = os.getenv("DATABASE_URL")
    if db is None:
        raise RuntimeError("DATABASE_URL is not set")
    conn = sqlite3.connect(db, check_same_thread=False)
    utils.create_phones_table_if_not_exist(conn)
    repo = repositories.SQLiteRepository(conn)
    sender = senders.HTTPX2Sender("localhost", 4000)
    app.state.get_bot = bot.Bot(repository=repo, sender=sender)
    yield
    conn.close()


def get_bot(request: fastapi.Request):
    return request.app.state.get_bot


app = fastapi.FastAPI(lifespan=lifespan)


@app.post("/reply")
async def reply(
        event: schemas.WhatsAppWebhookEvent,
        wa_bot = fastapi.Depends(get_bot),
    ):
    await wa_bot.send_message(event)


#
# if __name__ == "__main__":
#     uvicorn.run(app)
