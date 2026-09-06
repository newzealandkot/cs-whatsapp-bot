import os

import dotenv
import httpx2


dotenv.load_dotenv()

access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
recipient = os.getenv("WHATSAPP_RECIPIENT")

url = f"https://graph.facebook.com/v26.0/{phone_number_id}/messages"

headers ={
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

data = {
    "messaging_product": "whatsapp",
    "recipient_type": "individual",
    "to": recipient,
    "type": "text",
    "text": {
        "preview_url": False,
        "body": "Привет! Это сообщение отправлено из Python 🤖"
    },
}

response = httpx2.post(
    url,
    headers=headers,
    json=data,
)

print(response.status_code)
print(response.json())
