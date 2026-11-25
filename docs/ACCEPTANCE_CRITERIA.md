# Acceptance Criteria — SecureNotes MVP

Format: *Given / When / Then*. Identyfikatory odpowiadają pozycjom w `BACKLOG.csv`.

## US1 — Tworzenie notatki
- **Given** pusty magazyn, **when** użytkownik tworzy notatkę „Zakupy” z treścią „mleko”,
  **then** notatka otrzymuje unikalne `id`, `created_at` i pojawia się na liście.

## US2 — Lista notatek
- **Given** dwie notatki, **when** użytkownik pobiera listę,
  **then** otrzymuje obie, posortowane malejąco po dacie modyfikacji.

## US3 — Edycja notatki
- **Given** istniejąca notatka, **when** użytkownik zmienia treść,
  **then** treść jest zaktualizowana, a `updated_at` jest późniejsze niż `created_at`.

## US4 — Usuwanie notatki
- **Given** istniejąca notatka, **when** użytkownik ją usuwa, **then** nie ma jej na liście.
- **Given** nieistniejące `id`, **when** użytkownik usuwa notatkę, **then** zgłaszany jest błąd `NoteNotFound`.

## US5 — Walidacja
- Pusty tytuł, tytuł > 100 znaków lub treść > 10 000 znaków → `ValueError`, notatka nie zostaje zapisana.

## US6 — Szyfrowanie treści
- **Given** magazyn odblokowany hasłem, **when** użytkownik tworzy lub edytuje notatkę,
  **then** obiekt notatki przechowuje tylko `ciphertext` (AES-256-GCM), który nie zawiera tekstu jawnego.
- Dwukrotne zaszyfrowanie tej samej treści daje różne szyfrogramy (losowy nonce).

## US7 — Odczyt notatki hasłem
- **Given** notatka utworzona w magazynie, **when** użytkownik wywołuje `read(id)`,
  **then** otrzymuje dokładnie oryginalną treść (także z polskimi znakami).

## US8 — Ochrona przed błędnym hasłem
- **Given** istniejący magazyn (sól + verifier), **when** użytkownik otwiera go błędnym hasłem,
  **then** zgłaszany jest `InvalidPassword` i żadna treść nie jest zwracana.
- **Given** zmodyfikowany szyfrogram lub szyfrogram przeniesiony z innej notatki,
  **when** użytkownik go odczytuje, **then** zgłaszany jest `InvalidPassword`.

## Jakość (wszystkie sprinty)
- CI zielone: flake8, black --check, bandit, pytest.
- Pokrycie testami `src/` ≥ 80% (od Sprintu 2), SonarCloud Quality Gate = Passed.
