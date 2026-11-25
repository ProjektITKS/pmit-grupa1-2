# Sprint 2 — Plan i przegląd (29.10.2026 – 11.11.2026)

## Cel sprintu
Treść notatek jest przechowywana wyłącznie w postaci zaszyfrowanej i może zostać odczytana
tylko po podaniu poprawnego hasła; jakość kodu jest mierzona w SonarQube.

## Zakres (wybrane z BACKLOG.csv)
| ID | Tytuł | SP | Priorytet | Zależności |
|---|---|---|---|---|
| TECH3 | Moduł kryptograficzny | 5 | MUST | TECH2 |
| US6 | Szyfrowanie treści | 5 | MUST | TECH3 |
| US7 | Odczyt notatki hasłem | 3 | MUST | US6 |
| US8 | Ochrona przed błędnym hasłem | 3 | MUST | US7 |
| TECH4 | Analiza jakości SonarQube | 3 | SHOULD | TECH1 |
| | **Razem** | **19** | | |

Kolejność realizacji: TECH3 → US6 → US7 → US8. TECH4 równolegle (niezależne od kodu domenowego).
Velocity Sprintu 1 wyniosła 16 SP; 19 SP przyjęto świadomie, bo TECH4 realizuje osoba DevOps
niezaangażowana w US6–US8.

## Zadania techniczne
- `src/crypto.py`: wyprowadzanie klucza (scrypt, sól 128-bit), AES-256-GCM z losowym nonce 96-bit,
  identyfikator notatki jako dane uwierzytelniane (AAD) — blokuje podmianę szyfrogramów między notatkami.
- `NoteStore(password)`: treść szyfrowana przy `create`/`update`, odszyfrowywana w `read`;
  `verifier` wykrywa błędne hasło przy ponownym otwarciu magazynu.
- Jeden wyjątek `InvalidPassword` dla błędnego hasła i uszkodzonych danych (nie ujawnia, co zawiodło).
- CI: pomiar pokrycia (`pytest-cov`, próg 80%), raport `coverage.xml`, krok SonarCloud uruchamiany,
  gdy ustawiony jest sekret `SONAR_TOKEN`.
- Code review modułu kryptograficznego przez dwie osoby (reakcja na ryzyko R2).

## Ryzyka sprintu
- R2 (błędne użycie kryptografii) — wyłącznie biblioteka `cryptography`, testy nonce/AAD/tamperingu.
- R4 (brak doświadczenia z SonarQube) — krok Sonar warunkowy, nie blokuje pipeline'u do czasu konfiguracji.

## Przegląd sprintu (Sprint Review)
- Zrealizowano: TECH3, US6, US7, US8, TECH4 — **19/19 SP** (velocity: 19).
- Pokrycie testami `src/`: 99% (25 testów); CI zielony; Quality Gate SonarCloud: Passed.
- Do Sprintu 3: trwały zapis (US9), zmiana hasła (US10), wyszukiwanie (US11), raport (DOC1).
