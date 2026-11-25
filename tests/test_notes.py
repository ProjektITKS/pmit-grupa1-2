import pytest

from src.crypto import InvalidPassword
from src.notes import MAX_CONTENT_LEN, MAX_TITLE_LEN, NoteNotFound, NoteStore

PASSWORD = "correct horse battery staple"


@pytest.fixture
def store():
    return NoteStore(PASSWORD)


def test_create_note_is_listed(store):
    note = store.create("Zakupy", "mleko")
    assert note.id
    assert note.created_at is not None
    assert [n.id for n in store.list()] == [note.id]


def test_ids_are_unique(store):
    a = store.create("A")
    b = store.create("B")
    assert a.id != b.id


def test_list_sorted_by_last_modification(store):
    first = store.create("Pierwsza")
    second = store.create("Druga")
    store.update(first.id, "Pierwsza", "zmiana")
    assert [n.id for n in store.list()] == [first.id, second.id]


def test_update_changes_content_and_timestamp(store):
    note = store.create("Plan", "v1")
    store.update(note.id, "Plan", "v2")
    assert store.read(note.id) == "v2"
    assert note.updated_at >= note.created_at


def test_delete_removes_note(store):
    note = store.create("Do usunięcia")
    store.delete(note.id)
    assert store.list() == []


def test_delete_missing_note_raises(store):
    with pytest.raises(NoteNotFound):
        store.delete("missing")


@pytest.mark.parametrize(
    "title, content",
    [
        ("", "x"),
        ("   ", "x"),
        ("t" * (MAX_TITLE_LEN + 1), "x"),
        ("ok", "c" * (MAX_CONTENT_LEN + 1)),
    ],
)
def test_invalid_note_is_rejected(store, title, content):
    with pytest.raises(ValueError):
        store.create(title, content)
    assert store.list() == []


# --- Sprint 2: szyfrowanie (US6-US8) ---


def test_content_is_stored_only_as_ciphertext(store):
    note = store.create("PIN", "1234 tajne")
    assert not hasattr(note, "content")
    assert "tajne" not in note.ciphertext


def test_read_returns_original_content(store):
    note = store.create("Hasła", "zażółć gęślą jaźń")
    assert store.read(note.id) == "zażółć gęślą jaźń"


def test_reopen_with_correct_password(store):
    reopened = NoteStore(PASSWORD, salt=store.salt, verifier=store.verifier)
    assert reopened.salt == store.salt


def test_reopen_with_wrong_password_is_rejected(store):
    with pytest.raises(InvalidPassword):
        NoteStore("wrong", salt=store.salt, verifier=store.verifier)


def test_tampered_ciphertext_is_rejected(store):
    note = store.create("Konto", "IBAN")
    note.ciphertext = note.ciphertext[:-4] + "AAAA"
    with pytest.raises(InvalidPassword):
        store.read(note.id)


def test_ciphertext_cannot_be_swapped_between_notes(store):
    a = store.create("A", "treść A")
    b = store.create("B", "treść B")
    b.ciphertext = a.ciphertext
    with pytest.raises(InvalidPassword):
        store.read(b.id)
