# Sprint 3 — Plan i przegląd (12.11.2026 – 25.11.2026)

## Cel sprintu
Notatki są trwale zapisywane w pliku wyłącznie w postaci zaszyfrowanej, użytkownik może zmienić hasło
i wyszukać notatkę po tytule; projekt jest gotowy do prezentacji na mini demo day (26.11.2026).

## Zakres (wybrane z BACKLOG.csv)
| ID | Tytuł | SP | Priorytet | Zależności |
|---|---|---|---|---|
| US9 | Trwały zapis notatek | 3 | MUST | US6 |
| DOC1 | Raport końcowy i demo | 3 | MUST | — |
| US10 | Zmiana hasła | 5 | SHOULD | US7 |
| US11 | Wyszukiwanie po tytule | 2 | SHOULD | US2 |
| US12 | Eksport kopii zapasowej | 3 | COULD | US9 |
| | **Razem** | **16** | | |

Kolejność realizacji: US9 → US10 → US11 → US12; DOC1 równolegle od połowy sprintu.
Średnia velocity z dwóch sprintów to 17,5 SP. Ze względu na sesję (ryzyko R6) zaplanowano 16 SP,
a US12 (COULD) jest pierwszym kandydatem do usunięcia ze sprintu.

## Zadania techniczne
- `NoteStore.save()` / `NoteStore.load()`: format JSON z polem `version`, parametrami KDF, solą, verifierem;
  zapis atomowy (plik tymczasowy + `os.replace`), treść notatek wyłącznie jako szyfrogram.
- `NoteStore.change_password()`: weryfikacja starego hasła (porównanie w stałym czasie), nowa sól,
  ponowne zaszyfrowanie wszystkich notatek.
- `NoteStore.search()`: wyszukiwanie po tytule bez rozróżniania wielkości liter (bez odszyfrowywania treści).
- Test potwierdzający brak tekstu jawnego i hasła w pliku danych (ryzyko R3).
- Scenariusz demonstracyjny `examples/demo.py`, raport końcowy `docs/RAPORT.md`.

## Ryzyka sprintu
- R5 (rozrost zakresu) i R6 (dostępność zespołu) — US12 jako bufor do wycięcia.
- R7 (kompatybilność formatu) — pole `version` i test odrzucania nieznanej wersji.

## Przegląd sprintu (Sprint Review)
- Zrealizowano: US9, US10, US11, DOC1 — **13/16 SP** (velocity: 13).
- **Nie zrealizowano US12** (eksport kopii zapasowej, COULD) — zgodnie z decyzją z planowania
  pozycja wraca do product backlogu jako kandydat do kolejnej wersji.
- 33 testy, pokrycie `src/` 99%, CI zielony, Quality Gate SonarCloud: Passed.
- Wszystkie pozycje MUST i SHOULD z backlogu zostały dostarczone; cel SMART z Project Chartera osiągnięty.
