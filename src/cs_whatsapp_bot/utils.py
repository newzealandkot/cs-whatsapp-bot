import os

from dotenv import load_dotenv


load_dotenv()


def build_payload_from_event(*, event, body):
    sender_number = event.entry[0].changes[0].value.messages[0].from_
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{sender_number}",
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
