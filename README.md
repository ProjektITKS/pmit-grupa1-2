# SecureNotes — aplikacja do zarządzania notatkami z szyfrowaniem treści

Projekt zaliczeniowy z przedmiotu *Zarządzanie projektami IT*.
Celem nie jest budowa rozbudowanego systemu, lecz przećwiczenie zwinnego prowadzenia projektu
(Scrum): Project Charter, rejestr ryzyk, backlog z user stories, planowanie sprintów,
CI/CD (GitHub Actions) i analiza jakości kodu (SonarQube).

## Wizja produktu
SecureNotes pozwala użytkownikowi:
- tworzyć, przeglądać, edytować i usuwać notatki,
- przechowywać treść notatek **wyłącznie w postaci zaszyfrowanej** (AES-256-GCM, klucz wyprowadzany z hasła),
- odczytać treść tylko po podaniu poprawnego hasła.

## Dokumentacja projektu
| Dokument | Opis |
|---|---|
| [PROJECT_CHARTER.md](PROJECT_CHARTER.md) | Karta projektu: cel SMART, zakres, interesariusze, kryteria sukcesu |
| [RISK_REGISTER.csv](RISK_REGISTER.csv) | Rejestr ryzyk |
| [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) | Wymagania funkcjonalne i niefunkcjonalne |
| [BACKLOG.csv](BACKLOG.csv) | Product backlog (user stories + zadania techniczne) |
| [docs/ACCEPTANCE_CRITERIA.md](docs/ACCEPTANCE_CRITERIA.md) | Kryteria akceptacji |
| [docs/DoR_DoD.md](docs/DoR_DoD.md) | Definition of Ready / Definition of Done |
| [docs/KANBAN.md](docs/KANBAN.md) | Przeniesienie backlogu na tablicę Kanban (GitHub Projects) |
| [SPRINT1_PLAN.md](SPRINT1_PLAN.md) | Plan i przegląd Sprintu 1 |

## Uruchomienie lokalne
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows:     .venv\Scripts\activate
pip install -r requirements.txt
flake8 && black --check . && bandit -r src -q && pytest -q
```

## CI/CD
Każdy push i pull request do `main` uruchamia pipeline GitHub Actions
(`.github/workflows/ci.yml`): flake8 → black → bandit → pytest.
