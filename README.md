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
| [SPRINT2_PLAN.md](SPRINT2_PLAN.md) | Plan i przegląd Sprintu 2 |
| [SPRINT3_PLAN.md](SPRINT3_PLAN.md) | Plan i przegląd Sprintu 3 |
| [docs/RETROSPECTIVES.md](docs/RETROSPECTIVES.md) | Retrospektywy sprintów |
| [docs/RAPORT.md](docs/RAPORT.md) | Raport końcowy (źródło do wersji PDF) |
| [CHANGELOG.md](CHANGELOG.md) | Zmiany w kolejnych sprintach |

## Demo
```bash
python -m examples.demo
```
Scenariusz: utworzenie notatek → zapis do pliku (bez tekstu jawnego) → odczyt hasłem →
odmowa przy błędnym haśle → wyszukiwanie → zmiana hasła.

## Projekt kryptograficzny
- Klucz 256-bit wyprowadzany z hasła przez **scrypt** (N=2^14, r=8, p=1) z losową solą 128-bit.
- Treść szyfrowana **AES-256-GCM** z losowym nonce 96-bit dla każdego zapisu;
  identyfikator notatki jest danymi uwierzytelnianymi (AAD), więc szyfrogramu nie da się
  przenieść do innej notatki.
- Błędne hasło jest wykrywane przez `verifier` (zaszyfrowana stała wartość).
- Błędne hasło i uszkodzone dane dają ten sam wyjątek `InvalidPassword`.
- Hasło ani jawna treść nie są zapisywane ani logowane. Używamy wyłącznie biblioteki `cryptography`.
- Plik danych (JSON) zawiera: `version`, parametry KDF, sól, verifier oraz notatki z szyfrogramem treści.
  Zapis jest atomowy (plik tymczasowy + `os.replace`).
- **Tytuły notatek nie są szyfrowane.** To świadomy kompromis, który pozwala wyszukiwać i listować
  notatki bez odszyfrowywania treści. Poufne informacje należy umieszczać w treści.

## Uruchomienie lokalne
```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows:     .venv\Scripts\activate
pip install -r requirements.txt
flake8 && black --check . && bandit -r src -q && pytest -q --cov=src
```

## CI/CD
Każdy push i pull request do `main` uruchamia pipeline GitHub Actions
(`.github/workflows/ci.yml`): flake8 → black → bandit → pytest z pokryciem (próg 80%) → SonarCloud.

Konfiguracja SonarCloud: import repozytorium w sonarcloud.io, wyłączenie *Automatic Analysis*,
dodanie sekretu repozytorium `SONAR_TOKEN` (Settings → Secrets and variables → Actions)
i ustawienie `sonar.organization` / `sonar.projectKey` w `sonar-project.properties`.
Bez sekretu krok Sonar jest pomijany, a reszta pipeline'u działa.
