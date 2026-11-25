# Tablica Kanban — GitHub Projects

Backlog jest utrzymywany w `BACKLOG.csv` i odwzorowany na tablicy **„SecureNotes — Kanban”**
w GitHub Projects (zakładka *Projects* repozytorium).

## Struktura tablicy
- Kolumny (pole *Status*): `Todo`, `In Progress`, `Done`.
- Pola: `Sprint` (Sprint 1 / Sprint 2 / Sprint 3 / Backlog), `Story Points`,
  `Priorytet` (MUST / SHOULD / COULD / WONT), `Typ` (User Story / Tech / Dokumentacja).
- Każda pozycja backlogu to issue z:
  - tytułem `ID: tytuł`,
  - etykietami typu i priorytetu,
  - milestonem odpowiadającym sprintowi,
  - kryteriami akceptacji jako checklistą,
  - zależnościami jako odnośnikami `#nr`.

## Import backlogu (automatyczny)
Skrypt `scripts/backlog_to_kanban.py` tworzy etykiety, milestones (sprinty), projekt, pola i issues
na podstawie `BACKLOG.csv`. Ustawia też pola kart i zamyka issues ze statusem `Done`.
Ponowne uruchomienie nie duplikuje danych.

```bash
gh auth login -s project
python scripts/backlog_to_kanban.py --repo ProjektITKS/pmit-grupa1-2
```

## Zasady pracy
- Karta przechodzi do `Done` dopiero po spełnieniu DoD (`docs/DoR_DoD.md`).
- Limit WIP w kolumnie `In Progress`: 1 karta na osobę.
- Pull request zamyka issue słowem kluczowym (`Closes #nr`).
