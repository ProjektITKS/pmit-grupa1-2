"""Model notatek i magazyn notatek z szyfrowaną treścią."""

import base64
import hmac
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Union
from uuid import uuid4

from src import crypto

MAX_TITLE_LEN = 100
MAX_CONTENT_LEN = 10_000
FILE_VERSION = 1
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

    # --- Sprint 3: wyszukiwanie, zmiana hasła, trwały zapis ---

    def search(self, query: str) -> List[Note]:
        """Notatki z ``query`` w tytule (bez rozróżniania wielkości liter)."""
        q = query.casefold()
        return [n for n in self.list() if q in n.title.casefold()]

    def change_password(self, old_password: str, new_password: str) -> None:
        """Weryfikuje stare hasło i szyfruje wszystkie notatki nowym kluczem."""
        if not hmac.compare_digest(
            crypto.derive_key(old_password, self.salt), self._key
        ):
            raise crypto.InvalidPassword()
        plaintexts = {note_id: self.read(note_id) for note_id in self._notes}
        new_salt = crypto.new_salt()
        new_key = crypto.derive_key(new_password, new_salt)
        for note_id, content in plaintexts.items():
            self._notes[note_id].ciphertext = crypto.encrypt(
                new_key, content, aad=note_id
            )
        self.salt, self._key = new_salt, new_key
        self.verifier = crypto.encrypt(new_key, _VERIFIER_PLAINTEXT)

    def save(self, path: Union[str, Path]) -> None:
        """Zapisuje magazyn do pliku JSON; treść notatek wyłącznie jako szyfrogram."""
        data = {
            "version": FILE_VERSION,
            "kdf": {
                "name": "scrypt",
                "n": crypto.SCRYPT_N,
                "r": crypto.SCRYPT_R,
                "p": crypto.SCRYPT_P,
            },
            "salt": base64.b64encode(self.salt).decode("ascii"),
            "verifier": self.verifier,
            "notes": [
                {
                    "id": n.id,
                    "title": n.title,
                    "ciphertext": n.ciphertext,
                    "created_at": n.created_at.isoformat(),
                    "updated_at": n.updated_at.isoformat(),
                }
                for n in self._notes.values()
            ],
        }
        path = Path(path)
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")
        os.replace(tmp, path)

    @classmethod
    def load(cls, path: Union[str, Path], password: str) -> "NoteStore":
        """Wczytuje magazyn z pliku; błędne hasło -> ``InvalidPassword``."""
        data = json.loads(Path(path).read_text("utf-8"))
        if data.get("version") != FILE_VERSION:
            raise ValueError(f"unsupported file version: {data.get('version')}")
        store = cls(
            password,
            salt=base64.b64decode(data["salt"]),
            verifier=data["verifier"],
        )
        for item in data["notes"]:
            note = Note(
                title=item["title"],
                ciphertext=item["ciphertext"],
                id=item["id"],
                created_at=datetime.fromisoformat(item["created_at"]),
                updated_at=datetime.fromisoformat(item["updated_at"]),
            )
            store._notes[note.id] = note
        return store
