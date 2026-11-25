# Retrospektywy sprintów

Format: *Co poszło dobrze / Co poszło źle / Działania na kolejny sprint*.

## Retrospektywa Sprintu 1 (28.10.2026)
**Co poszło dobrze**
- Zrealizowano 100% zaplanowanego zakresu (16 SP).
- CI skonfigurowane jako pierwsze — każda kolejna zmiana była od razu sprawdzana.
- Przesunięcie szyfrowania do Sprintu 2 pozwoliło skupić się na fundamencie.

**Co poszło źle**
- Szablon CI miał błąd (warunek na `secrets` w `if`) — stracono czas na diagnozę.
- Część kryteriów akceptacji była nieprecyzyjna i wymagała doprecyzowania w trakcie sprintu.
- Brak pomiaru pokrycia testami — nie wiadomo było, czy DoD jest spełnione.

**Działania (Sprint 2)**
- Dodać pomiar pokrycia z progiem 80% do CI i podpiąć SonarCloud (TECH4).
- Kryteria akceptacji pisać w formacie Given/When/Then przed rozpoczęciem pracy nad story.
- Moduł kryptograficzny poddać code review przez dwie osoby (ryzyko R2).
