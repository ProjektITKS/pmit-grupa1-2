import pytest

from src.notes import MAX_CONTENT_LEN, MAX_TITLE_LEN, NoteNotFound, NoteStore


@pytest.fixture
def store():
    return NoteStore()


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
    updated = store.update(note.id, "Plan", "v2")
    assert updated.content == "v2"
    assert updated.updated_at >= updated.created_at


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
