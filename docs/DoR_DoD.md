# Definition of Ready (DoR)
Pozycja backlogu może wejść do sprintu, gdy:
- ma opis w formacie user story (*Jako… chcę… aby…*) lub jasny opis zadania technicznego,
- ma kryteria akceptacji, które da się zweryfikować testem lub demonstracją,
- jest oszacowana w story points (≤ 5 SP; większe dzielimy),
- ma priorytet MoSCoW i rozpoznane zależności,
- spełnia INVEST (niezależna, negocjowalna, wartościowa, szacowalna, mała, testowalna).

# Definition of Done (DoD)
Pozycja jest skończona, gdy:
- kod jest w `main` przez pull request z co najmniej jednym code review,
- testy jednostkowe pokrywają nową funkcjonalność i przechodzą,
- pipeline CI jest zielony (flake8, black --check, bandit, pytest),
- spełnione są kryteria akceptacji z `docs/ACCEPTANCE_CRITERIA.md`,
- kod nie loguje ani nie zapisuje haseł i jawnej treści notatek,
- zaktualizowano dokumentację (README / backlog / plan sprintu) i status karty na tablicy Kanban.
