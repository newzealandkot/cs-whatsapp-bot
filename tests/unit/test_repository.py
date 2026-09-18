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


def test_try_claim_message_succeeds_for_new_message_id():
    repo = FakeRepository()
    assert repo.try_claim_message("message_id") is True


def test_try_claim_message_fails_for_already_claimed_message_id():
    repo = FakeRepository()
    repo.try_claim_message("message_id")
    assert repo.try_claim_message("message_id") is False


def test_release_message_claim_allows_reclaiming():
    repo = FakeRepository()
    repo.try_claim_message("message_id")
    repo.release_message_claim("message_id")
    assert repo.try_claim_message("message_id") is True
