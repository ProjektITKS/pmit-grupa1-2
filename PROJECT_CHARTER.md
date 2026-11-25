# Project Charter — SecureNotes (aplikacja do zarządzania notatkami z szyfrowaniem treści)

## Cel (SMART)
Do **26 listopada 2026** (mini demo day) dostarczyć MVP biblioteki/aplikacji SecureNotes, która:
- umożliwia tworzenie, listowanie, edycję i usuwanie notatek (tytuł + treść),
- przechowuje treść każdej notatki wyłącznie w postaci zaszyfrowanej algorytmem **AES-256-GCM**
  z kluczem wyprowadzanym z hasła użytkownika (KDF **scrypt**),
- odmawia odszyfrowania przy błędnym haśle lub zmodyfikowanym szyfrogramie.

Mierniki: 100% kryteriów akceptacji z `docs/ACCEPTANCE_CRITERIA.md` spełnionych na demo,
pokrycie testami modułów `src/` ≥ 80%, 0 podatności o wysokiej ważności w bandit/SonarQube,
pipeline CI zielony na gałęzi `main`.

## Zakres (In / Out)
**IN:**
- model notatki i operacje CRUD,
- szyfrowanie/odszyfrowanie treści (AES-256-GCM, scrypt, losowa sól i nonce),
- trwały zapis notatek do pliku JSON (treść tylko jako szyfrogram),
- zmiana hasła (ponowne szyfrowanie notatek), wyszukiwanie po tytule,
- testy jednostkowe, CI (GitHub Actions), analiza jakości (SonarQube),
- dokumentacja projektowa i raport końcowy.

**OUT:**
- konta użytkowników, logowanie, współdzielenie notatek między użytkownikami,
- synchronizacja w chmurze, aplikacja mobilna, rozbudowany interfejs graficzny,
- odzyskiwanie zapomnianego hasła (świadoma decyzja — brak „tylnej furtki”),
- własne implementacje algorytmów kryptograficznych (używamy biblioteki `cryptography`).

## Interesariusze
- **Klient / Product Owner** — prowadzący zajęcia — ustala priorytety, akceptuje przyrosty.
- **Scrum Master / PM** — członek zespołu — prowadzi backlog, rejestr ryzyk, ceremonie.
- **Zespół deweloperski** (dev, tester, DevOps) — implementacja, testy, pipeline CI/CD.
- **Użytkownik końcowy** — osoba przechowująca poufne notatki (hasła, dane prywatne, notatki służbowe).

## Kryteria sukcesu
- Demo na mini demo day przechodzi wszystkie scenariusze z `docs/ACCEPTANCE_CRITERIA.md`.
- W pliku z danymi nie występuje jawny tekst żadnej notatki (weryfikowane testem).
- Pipeline CI zielony (flake8, black, bandit, pytest), wynik SonarQube Quality Gate = *Passed*.
- Dokumentacja (charter, backlog, ryzyka, plany sprintów, retrospektywy, raport) kompletna.

## Założenia
- Zespół 4 osób (fikcyjny), 3 sprinty po 2 tygodnie: 15.10–28.10, 29.10–11.11, 12.11–25.11.2026.
- Python 3.12, biblioteka `cryptography` jako zaufana implementacja AES-GCM i scrypt.
- Interfejs: moduł Pythona (API) wykorzystywany w testach i demo; UI nie jest priorytetem.

## Ograniczenia
- Czas: 6 tygodni, ok. 4 h pracy zespołu tygodniowo.
- Brak serwera i bazy danych — przechowywanie lokalne (pamięć / plik JSON).
- Repozytorium prywatne na GitHub, darmowe narzędzia (GitHub Actions, SonarCloud).

## Główne ryzyka
Szczegóły, ocena i reakcje: [RISK_REGISTER.csv](RISK_REGISTER.csv). Najważniejsze:
utrata hasła = utrata danych, błędne użycie kryptografii, wyciek jawnej treści (logi, pliki tymczasowe),
rozrost zakresu, brak doświadczenia z CI/SonarQube.
