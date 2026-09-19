def extract_contact_from_event(event):
    messages = event.entry[0].changes[0].value.messages
    if not messages:
        return None
    message = messages[0]
    if message.text is None:
        return None
    return message.from_


def extract_message_id_from_event(event):
    messages = event.entry[0].changes[0].value.messages
    if not messages:
        return None
    return messages[0].id


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


def create_processed_messages_table_if_not_exist(conn):
    create_table_processed_messages = """
            CREATE TABLE IF NOT EXISTS processed_messages (
                message_id TEXT PRIMARY KEY
            )
            """
    conn.execute(create_table_processed_messages)
    conn.commit()
