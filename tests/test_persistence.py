import json

import pytest

from src.crypto import InvalidPassword
from src.notes import NoteStore

PASSWORD = "stare-haslo"


@pytest.fixture
def store():
    s = NoteStore(PASSWORD)
    s.create("Bank", "PIN 4321")
    s.create("Lista zakupów", "chleb, masło")
    s.create("Zakupy świąteczne", "prezenty")
    return s


# --- US9: trwały zapis ---


def test_save_and_load_roundtrip(store, tmp_path):
    path = tmp_path / "data.notes.json"
    store.save(path)
    loaded = NoteStore.load(path, PASSWORD)
    assert {n.id for n in loaded.list()} == {n.id for n in store.list()}
    for note in store.list():
        assert loaded.read(note.id) == store.read(note.id)
        assert loaded.get(note.id).updated_at == note.updated_at


def test_file_contains_no_plaintext(store, tmp_path):
    path = tmp_path / "data.notes.json"
    store.save(path)
    raw = path.read_text("utf-8")
    for secret in ("PIN 4321", "chleb", "prezenty", PASSWORD):
        assert secret not in raw
    assert not (tmp_path / "data.notes.json.tmp").exists()


def test_load_with_wrong_password_is_rejected(store, tmp_path):
    path = tmp_path / "data.notes.json"
    store.save(path)
    with pytest.raises(InvalidPassword):
        NoteStore.load(path, "zle-haslo")


def test_load_unsupported_version_is_rejected(store, tmp_path):
    path = tmp_path / "data.notes.json"
    store.save(path)
    data = json.loads(path.read_text("utf-8"))
    data["version"] = 999
    path.write_text(json.dumps(data), "utf-8")
    with pytest.raises(ValueError):
        NoteStore.load(path, PASSWORD)


# --- US10: zmiana hasła ---


def test_change_password_reencrypts_notes(store, tmp_path):
    before = {n.id: n.ciphertext for n in store.list()}
    store.change_password(PASSWORD, "nowe-haslo")
    for note in store.list():
        assert note.ciphertext != before[note.id]
        assert store.read(note.id)

    path = tmp_path / "data.notes.json"
    store.save(path)
    assert NoteStore.load(path, "nowe-haslo").read(store.list()[0].id)
    with pytest.raises(InvalidPassword):
        NoteStore.load(path, PASSWORD)


def test_change_password_requires_old_password(store):
    with pytest.raises(InvalidPassword):
        store.change_password("zle-haslo", "nowe-haslo")


# --- US11: wyszukiwanie po tytule ---


def test_search_is_case_insensitive(store):
    titles = {n.title for n in store.search("ZAKUP")}
    assert titles == {"Lista zakupów", "Zakupy świąteczne"}


def test_search_without_match_returns_empty(store):
    assert store.search("urlop") == []
