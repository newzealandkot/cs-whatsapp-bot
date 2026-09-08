import os

from dotenv import load_dotenv


load_dotenv()


def make_whatsapp_message_payload(*, recipient, body):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{recipient}",
        "type": "text",
        "text": {
            "preview_url": False,
            "body": f"{body}"
        },
    }
    return payload


def make_headers_from_env():
    token = os.getenv("WHATSAPP_ACCESS_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    return headers
