"""Model notatek i magazyn notatek z szyfrowaną treścią (Sprint 2)."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from src import crypto

MAX_TITLE_LEN = 100
MAX_CONTENT_LEN = 10_000
_VERIFIER_PLAINTEXT = "securenotes-verifier"


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
    """Notatka; treść przechowywana wyłącznie jako szyfrogram."""

    title: str
    ciphertext: str = ""
    id: str = field(default_factory=lambda: uuid4().hex)
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


class NoteStore:
    """Magazyn notatek odblokowywany hasłem użytkownika.

    Z hasła i soli wyprowadzany jest klucz AES-256. ``verifier`` to zaszyfrowana
    stała wartość, pozwalająca wykryć błędne hasło przy ponownym otwarciu magazynu.
    """

    def __init__(
        self,
        password: str,
        salt: Optional[bytes] = None,
        verifier: Optional[str] = None,
    ) -> None:
        self.salt = salt or crypto.new_salt()
        self._key = crypto.derive_key(password, self.salt)
        if verifier is None:
            self.verifier = crypto.encrypt(self._key, _VERIFIER_PLAINTEXT)
        else:
            if crypto.decrypt(self._key, verifier) != _VERIFIER_PLAINTEXT:
                raise crypto.InvalidPassword()
            self.verifier = verifier
        self._notes: Dict[str, Note] = {}

    def create(self, title: str, content: str = "") -> Note:
        validate(title, content)
        note = Note(title=title.strip())
        note.ciphertext = crypto.encrypt(self._key, content, aad=note.id)
        self._notes[note.id] = note
        return note

    def get(self, note_id: str) -> Note:
        try:
            return self._notes[note_id]
        except KeyError:
            raise NoteNotFound(note_id) from None

    def read(self, note_id: str) -> str:
        """Zwraca odszyfrowaną treść notatki."""
        note = self.get(note_id)
        return crypto.decrypt(self._key, note.ciphertext, aad=note.id)

    def list(self) -> List[Note]:
        return sorted(self._notes.values(), key=lambda n: n.updated_at, reverse=True)

    def update(self, note_id: str, title: str, content: str) -> Note:
        note = self.get(note_id)
        validate(title, content)
        note.title = title.strip()
        note.ciphertext = crypto.encrypt(self._key, content, aad=note.id)
        note.updated_at = _now()
        return note

    def delete(self, note_id: str) -> None:
        self.get(note_id)
        del self._notes[note_id]
