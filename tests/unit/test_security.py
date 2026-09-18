import hashlib
import hmac

from src.cs_whatsapp_bot import security


SECRET = "test_app_secret"
BODY = b'{"object": "whatsapp_business_account"}'


def sign(secret, body):
    digest = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_verify_signature_accepts_correct_signature():
    header = sign(SECRET, BODY)
    assert security.verify_signature(SECRET, BODY, header) is True


def test_verify_signature_rejects_missing_header():
    assert security.verify_signature(SECRET, BODY, None) is False


def test_verify_signature_rejects_header_without_prefix():
    digest = hmac.new(SECRET.encode(), BODY, hashlib.sha256).hexdigest()
    assert security.verify_signature(SECRET, BODY, digest) is False


def test_verify_signature_rejects_empty_value_after_prefix():
    assert security.verify_signature(SECRET, BODY, "sha256=") is False


def test_verify_signature_rejects_non_hex_characters():
    header = "sha256=" + "z" * 64
    assert security.verify_signature(SECRET, BODY, header) is False


def test_verify_signature_rejects_value_with_embedded_whitespace():
    digest = hmac.new(SECRET.encode(), BODY, hashlib.sha256).hexdigest()
    tampered = digest[:32] + " " + digest[32:]
    assert security.verify_signature(SECRET, BODY, f"sha256={tampered}") is False


def test_verify_signature_rejects_leading_or_trailing_whitespace_around_header():
    digest = hmac.new(SECRET.encode(), BODY, hashlib.sha256).hexdigest()
    assert security.verify_signature(SECRET, BODY, f" sha256={digest}") is False
    assert security.verify_signature(SECRET, BODY, f"sha256={digest} ") is False


def test_verify_signature_rejects_too_short_digest():
    header = "sha256=" + "a" * 63
    assert security.verify_signature(SECRET, BODY, header) is False


def test_verify_signature_rejects_too_long_digest():
    header = "sha256=" + "a" * 65
    assert security.verify_signature(SECRET, BODY, header) is False


def test_verify_signature_rejects_wrong_value():
    header = "sha256=" + "a" * 64
    assert security.verify_signature(SECRET, BODY, header) is False


def test_verify_signature_rejects_signature_of_different_body():
    other_body = b'{"object": "different"}'
    header = sign(SECRET, other_body)
    assert security.verify_signature(SECRET, BODY, header) is False
