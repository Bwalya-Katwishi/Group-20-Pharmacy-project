"""PasswordHasher — GRASP Pure Fabrication. Never store plaintext."""

import hashlib
import hmac
import secrets


class PasswordHasher:
    ITERATIONS = 210_000

    @classmethod
    def hash(cls, password: str) -> tuple[str, str]:
        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), cls.ITERATIONS
        ).hex()
        return digest, salt

    @classmethod
    def verify(cls, password: str, password_hash: str, password_salt: str) -> bool:
        if not password_hash or not password_salt:
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), password_salt.encode("utf-8"), cls.ITERATIONS
        ).hex()
        return hmac.compare_digest(digest, password_hash)
