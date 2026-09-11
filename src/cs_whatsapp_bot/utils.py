import os

from dotenv import load_dotenv


load_dotenv()


def extract_contact_from_event(event):
    return event.entry[0].changes[0].value.messages[0].from_


def build_output_payload(*, contact, body):
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{contact}",
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
