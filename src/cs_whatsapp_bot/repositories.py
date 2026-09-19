import sqlite3


class FakeConnection:

    def __init__(self):
        self.commited = False

    def commit(self):
        self.commited = True


class FakeRepository:

    def __init__(self, session=None):
        self._users = set()
        self._processed_messages = set()

    def add(self, user):
        self._users.add(user)

    def get(self, user):
        return next(
            (item for item in self._users if item == user),
            None,
        )

    def try_claim_message(self, message_id):
        if message_id in self._processed_messages:
            return False
        self._processed_messages.add(message_id)
        return True

    def release_message_claim(self, message_id):
        self._processed_messages.discard(message_id)

    def try_claim_contact(self, phone):
        if phone in self._users:
            return False
        self._users.add(phone)
        return True

    def release_contact_claim(self, phone):
        self._users.discard(phone)


class SQLiteRepository:

    def __init__(self, connection):
        self.conn = connection

    def add(self, phone):
        self.conn.execute(
            "INSERT INTO phones (phone) VALUES (?)",
            (phone,),
        )
        self.conn.commit()

    def get(self, phone):
        cursor = self.conn.execute(
            "SELECT phone FROM phones WHERE phone = ?",
            (phone,),
        )
        result = cursor.fetchone()
        return result if result is None else result[0]

    def try_claim_message(self, message_id):
        try:
            self.conn.execute(
                "INSERT INTO processed_messages (message_id) VALUES (?)",
                (message_id,),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False

    def release_message_claim(self, message_id):
        self.conn.execute(
            "DELETE FROM processed_messages WHERE message_id = ?",
            (message_id,),
        )
        self.conn.commit()

    def try_claim_contact(self, phone):
        try:
            self.conn.execute(
                "INSERT INTO phones (phone) VALUES (?)",
                (phone,),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False

    def release_contact_claim(self, phone):
        self.conn.execute(
            "DELETE FROM phones WHERE phone = ?",
            (phone,),
        )
        self.conn.commit()
