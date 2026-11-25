# Sprint 1 — Plan i przegląd (15.10.2026 – 28.10.2026)

## Cel sprintu
Przygotować fundament projektu: dokumentację startową (charter, wymagania, ryzyka, backlog),
działający pipeline CI oraz model notatek z operacjami CRUD (jeszcze bez szyfrowania).

## Zakres (wybrane z BACKLOG.csv, priorytet MoSCoW)
| ID | Tytuł | SP | Priorytet | Zależności |
|---|---|---|---|---|
| TECH1 | Pipeline CI | 2 | MUST | — |
| TECH2 | Model danych notatki | 3 | MUST | — |
| US1 | Tworzenie notatki | 3 | MUST | TECH2 |
| US2 | Lista notatek | 2 | MUST | US1 |
| US3 | Edycja notatki | 2 | MUST | US1 |
| US4 | Usuwanie notatki | 1 | MUST | US1 |
| US5 | Walidacja notatki | 2 | SHOULD | US1 |
| TECH5 | Tablica Kanban | 1 | SHOULD | — |
| | **Razem** | **16** | | |

Kolejność realizacji: TECH1 → TECH2 → US1 → (US2, US3, US4 równolegle) → US5. TECH5 równolegle.

## Zadania techniczne
- Dostosowanie szkieletu repozytorium do tematu (README, charter, ryzyka, backlog).
- Spisanie wymagań funkcjonalnych i niefunkcjonalnych (`docs/REQUIREMENTS.md`).
- Poprawa workflow CI (błędny warunek `secrets` w `if`, bandit bez `|| true`, konfiguracja flake8 zgodna z black).
- Implementacja `src/notes.py` (Note, NoteStore, walidacja) + testy jednostkowe.
- Import backlogu do GitHub Projects (instrukcja: `docs/KANBAN.md`).

## Definition of Done
Zgodnie z [docs/DoR_DoD.md](docs/DoR_DoD.md).

## Ryzyka sprintu
- R4 (brak doświadczenia z CI) — CI konfigurowane jako pierwsze zadanie sprintu.
- R5 (rozrost zakresu) — szyfrowanie celowo przesunięte do Sprintu 2.

## Przegląd sprintu (Sprint Review)
- Zrealizowano: TECH1, TECH2, TECH5, US1–US5 — **16/16 SP** (velocity: 16).
- Pipeline CI zielony na `main`.
- Do Sprintu 2 przechodzi: szyfrowanie treści (TECH3, US6–US8) i SonarQube (TECH4).
