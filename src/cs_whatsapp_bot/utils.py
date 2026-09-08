def make_whatsapp_message_payload(recipient, body):
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
