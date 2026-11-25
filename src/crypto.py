"""Szyfrowanie treści notatek: AES-256-GCM, klucz wyprowadzany z hasła przez scrypt."""

import base64
import os

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_LEN = 16
NONCE_LEN = 12
KEY_LEN = 32
SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


class InvalidPassword(Exception):
    """Błędne hasło albo zmodyfikowany / uszkodzony szyfrogram."""

    def __init__(self) -> None:
        super().__init__("invalid password or corrupted data")


def new_salt() -> bytes:
    return os.urandom(SALT_LEN)


def derive_key(password: str, salt: bytes) -> bytes:
    if not password:
        raise ValueError("password must not be empty")
    kdf = Scrypt(salt=salt, length=KEY_LEN, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P)
    return kdf.derive(password.encode("utf-8"))


def encrypt(key: bytes, plaintext: str, aad: str = "") -> str:
    """Zwraca base64(nonce || szyfrogram || tag)."""
    nonce = os.urandom(NONCE_LEN)
    ct = AESGCM(key).encrypt(nonce, plaintext.encode("utf-8"), aad.encode("utf-8"))
    return base64.b64encode(nonce + ct).decode("ascii")


def decrypt(key: bytes, token: str, aad: str = "") -> str:
    try:
        raw = base64.b64decode(token, validate=True)
        nonce, ct = raw[:NONCE_LEN], raw[NONCE_LEN:]
        return AESGCM(key).decrypt(nonce, ct, aad.encode("utf-8")).decode("utf-8")
    except (InvalidTag, ValueError):
        raise InvalidPassword() from None
