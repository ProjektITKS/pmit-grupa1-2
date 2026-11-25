# Raport końcowy — SecureNotes
### Aplikacja do zarządzania notatkami z szyfrowaniem treści

Przedmiot: *Zarządzanie projektami IT* · Okres realizacji: 15.10.2026 – 25.11.2026 · Repozytorium: `pmit-grupa1-2`

---

## 1. Opis projektu
SecureNotes to biblioteka w języku Python do zarządzania notatkami, w której treść każdej notatki
jest przechowywana wyłącznie w postaci zaszyfrowanej. Projekt realizowano w metodyce Scrum
w trzech dwutygodniowych sprintach. Celem było przećwiczenie zwinnego zarządzania projektem
(karta projektu, rejestr ryzyk, backlog, planowanie sprintów, CI/CD, analiza jakości kodu),
a nie budowa rozbudowanego produktu.

**Cel SMART** (z [Project Chartera](../PROJECT_CHARTER.md)): do 26.11.2026 dostarczyć MVP umożliwiające
operacje CRUD na notatkach, przechowujące treść wyłącznie jako szyfrogram AES-256-GCM z kluczem
wyprowadzanym z hasła (scrypt) i odmawiające odczytu przy błędnym haśle — przy zielonym CI,
pokryciu testami ≥ 80% i pozytywnym Quality Gate SonarQube.

**Zakres IN:** CRUD notatek, szyfrowanie treści, trwały zapis do pliku, zmiana hasła, wyszukiwanie po tytule,
testy, CI, SonarQube, dokumentacja.
**Zakres OUT:** konta użytkowników, synchronizacja w chmurze, współdzielenie notatek, odzyskiwanie hasła,
rozbudowany interfejs graficzny.

**Architektura rozwiązania:**
- `src/crypto.py` — wyprowadzanie klucza (scrypt: N=2^14, r=8, p=1, sól 128-bit), szyfrowanie
  AES-256-GCM (losowy nonce 96-bit, identyfikator notatki jako AAD).
- `src/notes.py` — model `Note` i magazyn `NoteStore` (CRUD, walidacja, wyszukiwanie, zmiana hasła,
  zapis/odczyt JSON z wersjonowaniem formatu).
- `tests/` — 33 testy jednostkowe; `examples/demo.py` — scenariusz demonstracyjny.

## 2. Zespół
Zespół fikcyjny, 4 osoby, role zgodne ze Scrumem:

| Rola | Odpowiedzialność |
|---|---|
| Product Owner (prowadzący) | Priorytety backlogu, akceptacja przyrostów |
| Scrum Master / PM | Ceremonie, backlog, rejestr ryzyk, raport |
| Developer (kryptografia) | Moduł `crypto`, model notatek |
| Developer / Tester | Testy jednostkowe, kryteria akceptacji, code review |
| DevOps | GitHub Actions, SonarCloud, tablica Kanban |

Ceremonie: planowanie sprintu (początek sprintu), cotygodniowy stand-up (10 min),
przegląd i retrospektywa (koniec sprintu).

## 3. Wymagania i backlog
Wymagania funkcjonalne (FR1–FR11) i niefunkcjonalne (NFR1–NFR8) opisano w
[docs/REQUIREMENTS.md](REQUIREMENTS.md). Każde wymaganie funkcjonalne ma odpowiadającą mu user story
w [BACKLOG.csv](../BACKLOG.csv), a kryteria akceptacji w formacie Given/When/Then —
w [docs/ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md). Priorytety nadano metodą MoSCoW.

| ID | Tytuł | SP | Priorytet | Sprint | Status |
|---|---|---|---|---|---|
| TECH1 | Pipeline CI | 2 | MUST | 1 | Done |
| TECH2 | Model danych notatki | 3 | MUST | 1 | Done |
| TECH5 | Tablica Kanban | 1 | SHOULD | 1 | Done |
| US1 | Tworzenie notatki | 3 | MUST | 1 | Done |
| US2 | Lista notatek | 2 | MUST | 1 | Done |
| US3 | Edycja notatki | 2 | MUST | 1 | Done |
| US4 | Usuwanie notatki | 1 | MUST | 1 | Done |
| US5 | Walidacja notatki | 2 | SHOULD | 1 | Done |
| TECH3 | Moduł kryptograficzny | 5 | MUST | 2 | Done |
| US6 | Szyfrowanie treści | 5 | MUST | 2 | Done |
| US7 | Odczyt notatki hasłem | 3 | MUST | 2 | Done |
| US8 | Ochrona przed błędnym hasłem | 3 | MUST | 2 | Done |
| TECH4 | Analiza jakości SonarQube | 3 | SHOULD | 2 | Done |
| US9 | Trwały zapis notatek | 3 | MUST | 3 | Done |
| US10 | Zmiana hasła | 5 | SHOULD | 3 | Done |
| US11 | Wyszukiwanie po tytule | 2 | SHOULD | 3 | Done |
| DOC1 | Raport końcowy i demo | 3 | MUST | 3 | Done |
| US12 | Eksport kopii zapasowej | 3 | COULD | — | Todo (poza MVP) |
| US13 | Tagi notatek | 2 | WONT | — | Todo (poza MVP) |

Backlog przeniesiono na tablicę Kanban w GitHub Projects ([docs/KANBAN.md](KANBAN.md)).

> 📷 *[Zrzut ekranu: tablica Kanban w GitHub Projects — `docs/img/kanban.png`]*

## 4. Przebieg sprintów

| Sprint | Okres | Cel | Plan (SP) | Wykonano (SP) |
|---|---|---|---|---|
| 1 | 15.10 – 28.10 | Fundament: dokumentacja, CI, CRUD | 16 | 16 |
| 2 | 29.10 – 11.11 | Szyfrowanie treści, SonarQube | 19 | 19 |
| 3 | 12.11 – 25.11 | Trwały zapis, zmiana hasła, wyszukiwanie, raport | 16 | 13 |
| | | **Razem** | **51** | **48** |

Średnia velocity: 16 SP / sprint. W Sprincie 3 świadomie nie zrealizowano US12 (COULD),
która pełniła rolę bufora na wypadek ograniczonej dostępności zespołu w czasie sesji.
Szczegóły: [SPRINT1_PLAN.md](../SPRINT1_PLAN.md), [SPRINT2_PLAN.md](../SPRINT2_PLAN.md),
[SPRINT3_PLAN.md](../SPRINT3_PLAN.md), retrospektywy: [docs/RETROSPECTIVES.md](RETROSPECTIVES.md).

## 5. Analiza ryzyk
Pełny rejestr: [RISK_REGISTER.csv](../RISK_REGISTER.csv).

| ID | Ryzyko | P | W | Reakcja | Stan na koniec projektu |
|---|---|---|---|---|---|
| R1 | Utrata hasła = utrata danych | Śr. | Wys. | Komunikat, brak „tylnej furtki” | Otwarte (US12 poza MVP) |
| R2 | Błędne użycie kryptografii | Śr. | Wys. | Biblioteka `cryptography`, AES-GCM + scrypt, review x2 | Monitorowane |
| R3 | Wyciek jawnej treści | Nis. | Wys. | Test braku plaintextu w pliku, bandit | Monitorowane |
| R4 | Brak doświadczenia z CI/SonarQube | Śr. | Śr. | Szablon CI, małe kroki | Zamknięte |
| R5 | Rozrost zakresu | Wys. | Śr. | MoSCoW, timeboxing, lista OUT | Wystąpiło — US12 wycięte |
| R6 | Ograniczona dostępność zespołu | Wys. | Śr. | Stand-upy, małe zadania | Wystąpiło w S3 — zamknięte |
| R7 | Kompatybilność formatu pliku | Nis. | Śr. | Pole `version`, test | Monitorowane |

Dwa ryzyka (R5, R6) zmaterializowały się w Sprincie 3. Dzięki zaplanowanemu buforowi (US12 jako COULD)
nie wpłynęły na osiągnięcie celu projektu.

## 6. CI/CD i jakość kodu
Pipeline GitHub Actions (`.github/workflows/ci.yml`) uruchamiany przy każdym pushu i pull requeście do `main`:

1. **flake8** — analiza statyczna stylu i błędów,
2. **black --check** — zgodność formatowania,
3. **bandit** — analiza bezpieczeństwa kodu,
4. **pytest + pytest-cov** — 33 testy, próg pokrycia 80% (osiągnięto 99%),
5. **SonarCloud** — analiza jakości (bugs, vulnerabilities, code smells, duplikacje, pokrycie).

> 📷 *[Zrzut ekranu: zielony przebieg workflow CI w zakładce Actions — `docs/img/ci.png`]*

> 📷 *[Zrzut ekranu: dashboard SonarCloud z Quality Gate „Passed” — `docs/img/sonar.png`]*

> 📷 *[Zrzut ekranu: wynik `python -m examples.demo` — `docs/img/demo.png`]*

## 7. Wnioski
- **Wszystkie pozycje MUST i SHOULD zostały dostarczone**, cel SMART osiągnięty: 48 z 51 zaplanowanych SP.
- **CI od pierwszego dnia** (TECH1 jako pierwsze zadanie) pozwoliło wykrywać błędy przy każdej zmianie;
  szablon CI wymagał poprawek (błędny warunek na `secrets`), co potwierdziło zasadność ryzyka R4.
- **Priorytetyzacja MoSCoW z buforem COULD** sprawdziła się, gdy w Sprincie 3 spadła dostępność zespołu.
- **Testy jako kryteria akceptacji** (Given/When/Then → test jednostkowy) ułatwiły weryfikację DoD.
- **Kompromis projektowy:** tytuły notatek nie są szyfrowane (wyszukiwanie bez odszyfrowania).
  W kolejnej wersji warto rozważyć ich szyfrowanie lub indeks wyszukiwania oparty na HMAC.
- **Kierunki rozwoju:** eksport kopii zapasowej (US12), tagi (US13), prosty interfejs CLI/GUI,
  regulowane parametry KDF.
