from src.cs_whatsapp_bot import SQLiteRepository


def test_added_phone_can_be_retrieved(sqlite_session):
    phone = "phone_number"
    repo = SQLiteRepository(sqlite_session)
    repo.add(phone)
    retrieved_phone = repo.get(phone)
    assert retrieved_phone == phone


def test_get_returns_none_for_unknown_phone(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    assert repo.get("unknown") is None
