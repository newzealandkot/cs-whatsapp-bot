import sqlite3
import threading

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


def test_try_claim_message_succeeds_for_new_message_id(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    assert repo.try_claim_message("message_id") is True


def test_try_claim_message_fails_for_already_claimed_message_id(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    repo.try_claim_message("message_id")
    assert repo.try_claim_message("message_id") is False


def test_release_message_claim_allows_reclaiming(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    repo.try_claim_message("message_id")
    repo.release_message_claim("message_id")
    assert repo.try_claim_message("message_id") is True


def test_try_claim_message_leaves_connection_usable_after_losing_claim(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    repo.try_claim_message("message_id")
    repo.try_claim_message("message_id")
    assert sqlite_session.in_transaction is False
    assert repo.try_claim_message("another_message_id") is True


def test_try_claim_message_is_atomic_under_concurrent_threads(sqlite_file_path):
    message_id = "concurrent-message-id"
    barrier = threading.Barrier(2)
    results = []

    def attempt():
        conn = sqlite3.connect(sqlite_file_path)
        repo = SQLiteRepository(conn)
        barrier.wait()
        results.append(repo.try_claim_message(message_id))
        conn.close()

    threads = [threading.Thread(target=attempt) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert results.count(True) == 1
    assert results.count(False) == 1

    verify_conn = sqlite3.connect(sqlite_file_path)
    rows = verify_conn.execute(
        "SELECT message_id FROM processed_messages WHERE message_id = ?", (message_id,)
    ).fetchall()
    verify_conn.close()
    assert len(rows) == 1


def test_try_claim_contact_succeeds_for_new_phone(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    assert repo.try_claim_contact("phone_number") is True


def test_try_claim_contact_fails_for_already_claimed_phone(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    repo.try_claim_contact("phone_number")
    assert repo.try_claim_contact("phone_number") is False


def test_release_contact_claim_allows_reclaiming(sqlite_session):
    repo = SQLiteRepository(sqlite_session)
    repo.try_claim_contact("phone_number")
    repo.release_contact_claim("phone_number")
    assert repo.try_claim_contact("phone_number") is True


def test_try_claim_contact_is_atomic_under_concurrent_threads(sqlite_file_path):
    phone = "concurrent-phone-number"
    barrier = threading.Barrier(2)
    results = []

    def attempt():
        conn = sqlite3.connect(sqlite_file_path)
        repo = SQLiteRepository(conn)
        barrier.wait()
        results.append(repo.try_claim_contact(phone))
        conn.close()

    threads = [threading.Thread(target=attempt) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert results.count(True) == 1
    assert results.count(False) == 1

    verify_conn = sqlite3.connect(sqlite_file_path)
    rows = verify_conn.execute("SELECT phone FROM phones WHERE phone = ?", (phone,)).fetchall()
    verify_conn.close()
    assert len(rows) == 1
