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

## Retrospektywa Sprintu 2 (11.11.2026)
**Co poszło dobrze**
- Zrealizowano 100% zakresu (19 SP) mimo wyższego planu niż velocity Sprintu 1.
- Testy tamperingu i podmiany szyfrogramu wykryły na etapie review potrzebę użycia AAD.
- Próg pokrycia w CI wymusza pisanie testów razem z kodem.

**Co poszło źle**
- Konfiguracja SonarCloud (organizacja, wyłączenie Automatic Analysis, sekret) zajęła więcej czasu niż szacowano.
- Plan 19 SP był możliwy tylko dzięki równoległej pracy osoby DevOps — w Sprincie 3 dostępność zespołu będzie niższa (sesja).

**Działania (Sprint 3)**
- Planować zakres poniżej średniej velocity, z pozycją COULD jako buforem.
- Zacząć raport końcowy (DOC1) w połowie sprintu, a nie na jego końcu.
- Zbierać zrzuty ekranu z CI i SonarCloud na bieżąco do raportu.

## Retrospektywa Sprintu 3 (25.11.2026)
**Co poszło dobrze**
- Dostarczono wszystkie pozycje MUST i SHOULD; cel SMART osiągnięty przed demo.
- Bufor w postaci US12 (COULD) zadziałał — wycięcie go nie zagroziło celowi sprintu.
- Wcześniejsze rozpoczęcie raportu ograniczyło pracę na ostatnią chwilę.

**Co poszło źle**
- Velocity spadła do 13 SP (sesja) — potwierdziło się ryzyko R6.
- Tytuły notatek pozostają nieszyfrowane (świadomy kompromis na rzecz wyszukiwania), co powinno być
  wcześniej omówione z Product Ownerem.

**Wnioski na przyszłość**
- Decyzje projektowe wpływające na bezpieczeństwo (np. co jest szyfrowane) uzgadniać z PO już na etapie wymagań.
- Utrzymać praktyki: CI od pierwszego dnia, próg pokrycia, Given/When/Then, bufor COULD w planie sprintu.
