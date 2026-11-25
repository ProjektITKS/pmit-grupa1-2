import pytest

from src import crypto


@pytest.fixture(scope="module")
def key():
    return crypto.derive_key("secret", crypto.new_salt())


def test_key_is_256_bit(key):
    assert len(key) == 32


def test_same_password_and_salt_give_same_key():
    salt = crypto.new_salt()
    assert crypto.derive_key("pw", salt) == crypto.derive_key("pw", salt)


def test_different_salt_gives_different_key():
    assert crypto.derive_key("pw", crypto.new_salt()) != crypto.derive_key(
        "pw", crypto.new_salt()
    )


def test_empty_password_is_rejected():
    with pytest.raises(ValueError):
        crypto.derive_key("", crypto.new_salt())


def test_roundtrip(key):
    token = crypto.encrypt(key, "tajna notatka")
    assert "tajna" not in token
    assert crypto.decrypt(key, token) == "tajna notatka"


def test_nonce_is_random(key):
    assert crypto.encrypt(key, "to samo") != crypto.encrypt(key, "to samo")


def test_wrong_key_is_rejected(key):
    token = crypto.encrypt(key, "x")
    other = crypto.derive_key("other", crypto.new_salt())
    with pytest.raises(crypto.InvalidPassword):
        crypto.decrypt(other, token)


def test_wrong_aad_is_rejected(key):
    token = crypto.encrypt(key, "x", aad="note-1")
    with pytest.raises(crypto.InvalidPassword):
        crypto.decrypt(key, token, aad="note-2")


def test_malformed_token_is_rejected(key):
    with pytest.raises(crypto.InvalidPassword):
        crypto.decrypt(key, "not base64 !!!")
