from src.cs_whatsapp_bot import FakeConnection, FakeRepository


def test_added_phone_can_be_retrieved():
    phone = "phone_number"
    repo = FakeRepository()
    repo.add(phone)
    retrieved_phone = repo.get(phone)
    assert retrieved_phone == phone


def test_get_returns_none_for_unknown_phone():
    repo = FakeRepository()
    assert repo.get("unknown") is None


def test_can_commit_transaction():
    conn = FakeConnection()
    conn.commit()
    assert conn.commited
