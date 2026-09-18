import sqlite3
from contextlib import asynccontextmanager

import dotenv
import fastapi
import pydantic
from fastapi import status

from . import bot, config, repositories, schemas, security, senders, utils


dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    db = config.load_database_url()
    conn = sqlite3.connect(db, check_same_thread=False)
    utils.create_phones_table_if_not_exist(conn)
    repo = repositories.SQLiteRepository(conn)
    sender = senders.HTTPX2Sender("localhost", 4000)
    app.state.get_bot = bot.Bot(repository=repo, sender=sender)
    yield
    conn.close()


def get_bot(request: fastapi.Request):
    return request.app.state.get_bot


def get_settings() -> config.Settings:
    return config.load_settings()


def get_security_settings() -> config.SecuritySettings:
    return config.load_security_settings()


app = fastapi.FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def receive_webhook(
        request: fastapi.Request,
        wa_bot = fastapi.Depends(get_bot),
        security_settings: config.SecuritySettings = fastapi.Depends(get_security_settings),
    ):
    raw_body = await request.body()
    signature_header = request.headers.get("x-hub-signature-256")
    if not security.verify_signature(security_settings.whatsapp_app_secret, raw_body, signature_header):
        return fastapi.Response(status_code=status.HTTP_403_FORBIDDEN)
    try:
        event = schemas.WhatsAppWebhookEvent.model_validate_json(raw_body)
    except pydantic.ValidationError:
        return fastapi.Response(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
    await wa_bot.send_message(event)


@app.get("/webhook")
async def verify_webhook(
        request: fastapi.Request,
        settings: config.Settings = fastapi.Depends(get_settings),
    ):
    params = request.query_params
    if params.get("hub.verify_token") == settings.whatsapp_verify_token:
        return fastapi.responses.PlainTextResponse(params.get("hub.challenge", ""))
    return fastapi.Response(status_code=status.HTTP_403_FORBIDDEN)
