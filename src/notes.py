"""Model notatek i magazyn notatek w pamięci (Sprint 1: CRUD + walidacja)."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List
from uuid import uuid4

MAX_TITLE_LEN = 100
MAX_CONTENT_LEN = 10_000


class NoteNotFound(KeyError):
    """Notatka o podanym identyfikatorze nie istnieje."""


def _now() -> datetime:
    return datetime.now(timezone.utc)


def validate(title: str, content: str) -> None:
    if not title or not title.strip():
        raise ValueError("title must not be empty")
    if len(title) > MAX_TITLE_LEN:
        raise ValueError(f"title must be at most {MAX_TITLE_LEN} characters")
    if len(content) > MAX_CONTENT_LEN:
        raise ValueError(f"content must be at most {MAX_CONTENT_LEN} characters")


@dataclass
class Note:
    title: str
    content: str
    id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


class NoteStore:
    """Magazyn notatek przechowywany w pamięci."""

    def __init__(self) -> None:
        self._notes: Dict[str, Note] = {}

    def create(self, title: str, content: str = "") -> Note:
        validate(title, content)
        note = Note(title=title.strip(), content=content)
        self._notes[note.id] = note
        return note

    def get(self, note_id: str) -> Note:
        try:
            return self._notes[note_id]
        except KeyError:
            raise NoteNotFound(note_id) from None

    def list(self) -> List[Note]:
        return sorted(self._notes.values(), key=lambda n: n.updated_at, reverse=True)

    def update(self, note_id: str, title: str, content: str) -> Note:
        note = self.get(note_id)
        validate(title, content)
        note.title = title.strip()
        note.content = content
        note.updated_at = _now()
        return note

    def delete(self, note_id: str) -> None:
        self.get(note_id)
        del self._notes[note_id]
