# Changelog

## Sprint 3 (12.11–25.11.2026)
- Trwały zapis i odczyt magazynu z pliku JSON z wersjonowaniem formatu (US9).
- Zmiana hasła z ponownym zaszyfrowaniem wszystkich notatek (US10).
- Wyszukiwanie notatek po tytule (US11).
- Scenariusz demonstracyjny `examples/demo.py`, raport końcowy `docs/RAPORT.md` (DOC1).
- US12 (eksport kopii zapasowej) przesunięte poza MVP.

## Sprint 2 (29.10–11.11.2026)
- Moduł `src/crypto.py`: scrypt + AES-256-GCM, AAD = id notatki (TECH3).
- Treść notatek przechowywana wyłącznie jako szyfrogram, odczyt hasłem, wykrywanie błędnego hasła (US6–US8).
- Pomiar pokrycia testami (próg 80%) i integracja SonarCloud w CI (TECH4).

## Sprint 1 (15.10–28.10.2026)
- Dostosowanie szkieletu projektu do tematu: charter, wymagania, rejestr ryzyk, backlog, DoR/DoD.
- Naprawa pipeline'u CI (flake8, black, bandit, pytest) (TECH1).
- Model notatek z operacjami CRUD i walidacją (TECH2, US1–US5); tablica Kanban (TECH5).
