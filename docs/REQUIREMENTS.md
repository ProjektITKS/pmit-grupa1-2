# Wymagania — SecureNotes

## Wymagania funkcjonalne (FR)
| ID | Wymaganie | User story |
|---|---|---|
| FR1 | System umożliwia utworzenie notatki z tytułem i treścią; nadaje jej unikalny identyfikator i datę utworzenia. | US1 |
| FR2 | System umożliwia wyświetlenie listy notatek (id, tytuł, data modyfikacji) bez odszyfrowywania treści. | US2 |
| FR3 | System umożliwia edycję tytułu i treści istniejącej notatki; aktualizuje datę modyfikacji. | US3 |
| FR4 | System umożliwia usunięcie notatki po identyfikatorze. | US4 |
| FR5 | System odrzuca notatkę z pustym tytułem, tytułem > 100 znaków lub treścią > 10 000 znaków. | US5 |
| FR6 | System szyfruje treść notatki przed zapisaniem jej w magazynie. | US6 |
| FR7 | System odszyfrowuje treść notatki tylko po podaniu poprawnego hasła. | US7 |
| FR8 | System zgłasza czytelny błąd przy błędnym haśle lub zmodyfikowanym szyfrogramie i nie zwraca żadnej treści. | US8 |
| FR9 | System zapisuje i wczytuje notatki z pliku JSON, w którym treść występuje wyłącznie jako szyfrogram. | US9 |
| FR10 | System umożliwia zmianę hasła z ponownym zaszyfrowaniem wszystkich notatek. | US10 |
| FR11 | System umożliwia wyszukiwanie notatek po fragmencie tytułu (bez rozróżniania wielkości liter). | US11 |

## Wymagania niefunkcjonalne (NFR)
| ID | Kategoria | Wymaganie | Weryfikacja |
|---|---|---|---|
| NFR1 | Bezpieczeństwo | Treść szyfrowana AES-256-GCM (szyfrowanie uwierzytelnione), nonce 96-bit losowy dla każdego szyfrowania. | Test jednostkowy + code review |
| NFR2 | Bezpieczeństwo | Klucz wyprowadzany z hasła przez scrypt (N=2^14, r=8, p=1), losowa sól 128-bit. | Test jednostkowy |
| NFR3 | Bezpieczeństwo | Hasło ani jawna treść nie są zapisywane na dysku ani logowane. | Test (brak plaintextu w pliku) + bandit |
| NFR4 | Wydajność | Zaszyfrowanie lub odszyfrowanie notatki 10 000 znaków < 1 s na typowym laptopie. | Test czasowy / demo |
| NFR5 | Jakość | Pokrycie testami kodu w `src/` ≥ 80%; flake8 i black bez błędów. | CI + SonarQube |
| NFR6 | Jakość | SonarQube Quality Gate = Passed, 0 podatności o wysokiej ważności. | SonarQube |
| NFR7 | Przenośność | Działa na Python 3.12 na Windows i Linux. | CI (ubuntu) + lokalnie (Windows) |
| NFR8 | Prywatność | Dane przechowywane wyłącznie lokalnie, bez wysyłania do usług zewnętrznych (RODO). | Code review |

## Ocena wymagań względem Project Chartera i ryzyk
- **Spójność z celem:** każde FR wspiera cel SMART (CRUD + szyfrowanie + odmowa przy błędnym haśle); brak funkcji z listy OUT.
- **Zgodność z zakresem:** zakres IN jest w pełni pokryty przez FR1–FR11; FR12 (eksport kopii) pozostaje jako COULD.
- **Powiązanie z ryzykami:** NFR1–NFR2 ograniczają R2, NFR3 ogranicza R3, FR9 + pole `version` ogranicza R7, R1 jest zaadresowane decyzją projektową i komunikatem.
- **Weryfikowalność:** każde wymaganie ma wskazany sposób sprawdzenia (test, CI, demo).
