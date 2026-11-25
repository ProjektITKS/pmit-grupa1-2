"""Scenariusz demonstracyjny na mini demo day.

Uruchomienie z katalogu głównego repozytorium:  python -m examples.demo
"""

import tempfile
from pathlib import Path

from src.crypto import InvalidPassword
from src.notes import NoteStore


def main() -> None:
    path = Path(tempfile.mkdtemp()) / "demo.notes.json"

    print("1. Tworzenie notatek (US1, US6)")
    store = NoteStore("haslo-demo")
    bank = store.create("Bank", "PIN do karty: 4321")
    store.create("Lista zakupów", "chleb, masło, kawa")
    for note in store.list():
        print(f"   {note.title:<15} szyfrogram: {note.ciphertext[:40]}...")

    print("2. Zapis do pliku (US9) - w pliku brak tekstu jawnego")
    store.save(path)
    print(f"   'PIN' w pliku: {'PIN' in path.read_text('utf-8')}")

    print("3. Odczyt z poprawnym hasłem (US7)")
    loaded = NoteStore.load(path, "haslo-demo")
    print(f"   {loaded.read(bank.id)}")

    print("4. Próba odczytu z błędnym hasłem (US8)")
    try:
        NoteStore.load(path, "zle-haslo")
    except InvalidPassword as exc:
        print(f"   odmowa: {exc}")

    print("5. Wyszukiwanie po tytule (US11)")
    print(f"   'zakup' -> {[n.title for n in loaded.search('zakup')]}")

    print("6. Zmiana hasła (US10)")
    loaded.change_password("haslo-demo", "nowe-haslo")
    loaded.save(path)
    print(f"   nowe hasło: {NoteStore.load(path, 'nowe-haslo').read(bank.id)}")


if __name__ == "__main__":
    main()
