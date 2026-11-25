# Tablica Kanban — GitHub Projects

Backlog jest utrzymywany w `BACKLOG.csv` i odwzorowany na tablicy w GitHub Projects.

## Konfiguracja tablicy
1. Zakładka **Projects** repozytorium → **New project** → szablon **Board**.
2. Kolumny (pole *Status*): `Backlog`, `Todo (Sprint)`, `In Progress`, `Review`, `Done`.
3. Pola niestandardowe: `Sprint` (Iteration, 2 tygodnie od 15.10.2026), `Story Points` (Number),
   `Priorytet` (Single select: MUST / SHOULD / COULD / WONT), `Typ` (User Story / Tech / Dokumentacja).

## Import backlogu
Każdy wiersz `BACKLOG.csv` → osobny issue (tytuł `ID: tytuł`, w treści user story,
kryteria akceptacji jako checklista, zależności jako odnośniki `#nr`), dodany do projektu
z uzupełnionymi polami `Sprint`, `Story Points`, `Priorytet`, `Typ`.

## Zasady pracy
- Karta przechodzi do `Done` dopiero po spełnieniu DoD (`docs/DoR_DoD.md`).
- Limit WIP w kolumnie `In Progress`: 1 karta na osobę.
- Pull request zamyka issue słowem kluczowym (`Closes #nr`).
