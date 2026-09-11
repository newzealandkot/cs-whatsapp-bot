class FakeConnection:

    def __init__(self):
        self.commited = False

    def commit(self):
        self.commited = True


class FakeRepository:

    def __init__(self, session=None):
        self._users = set()

    def add(self, user):
        self._users.add(user)

    def get(self, user):
        return next(
            (item for item in self._users if item == user),
            None,
        )


class SQLiteRepository:

    def __init__(self, connection):
        self.conn = connection

    def add(self, phone):
        self.conn.execute(
            "INSERT INTO phones (phone) VALUES (?)",
            (phone,),
        )

    def get(self, phone):
        cursor = self.conn.execute(
            "SELECT phone FROM phones WHERE phone = ?",
            (phone,),
        )
        result = cursor.fetchone()
        return result if result is None else result[0]
