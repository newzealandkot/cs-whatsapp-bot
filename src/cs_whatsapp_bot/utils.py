import os


def extract_contact_from_event(event):
    messages = event.entry[0].changes[0].value.messages
    if not messages:
        return None
    message = messages[0]
    if message.text is None:
        return None
    return message.from_


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


def create_phones_table_if_not_exist(conn):
    create_table_phones = """
            CREATE TABLE IF NOT EXISTS phones (
                id INTEGER PRIMARY KEY,
                phone TEXT NOT NULL UNIQUE
            )
            """
    conn.execute(create_table_phones)
    conn.commit()
    # conn.close()
