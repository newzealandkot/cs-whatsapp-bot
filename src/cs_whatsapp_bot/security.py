import hashlib
import hmac
import re

SIGNATURE_PREFIX = "sha256="
_HEX_DIGEST_PATTERN = re.compile(r"^[0-9a-fA-F]{64}$")


def verify_signature(secret: str, body: bytes, signature_header: str | None) -> bool:
    if signature_header is None or not signature_header.startswith(SIGNATURE_PREFIX):
        return False
    provided_hex = signature_header[len(SIGNATURE_PREFIX):]
    if not _HEX_DIGEST_PATTERN.fullmatch(provided_hex):
        return False
    provided = bytes.fromhex(provided_hex)
    expected = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    return hmac.compare_digest(provided, expected)
