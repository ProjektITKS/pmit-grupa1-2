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

## Jakość (wszystkie sprinty)
- CI zielone: flake8, black --check, bandit, pytest.
