# Symulacja skrzyżowania — Plac Jana Pawła II

Projekt przedstawia symulację ruchu drogowego na skrzyżowaniu wzorowanym na Placu Jana Pawła II. Symulacja została napisana w Pythonie z wykorzystaniem biblioteki Pygame. Celem projektu jest odwzorowanie zachowania różnych uczestników ruchu oraz testowanie prostych mechanizmów sterowania ruchem.

## Funkcjonalności

Projekt zawiera:

* symulację ruchu samochodów osobowych,
* pojazdy dostawcze,
* autobusy poruszające się po buspasach,
* tramwaje poruszające się po torowisku,
* pojazdy uprzywilejowane,
* adaptacyjne sterowanie sygnalizacją świetlną,
* wykrywanie długości kolejek,
* reakcję pojazdów na pojazdy uprzywilejowane,
* przystanki autobusowe,
* podstawowe statystyki ruchu,
* wizualizację skrzyżowania w Pygame.

## Model ruchu

Ruch pojazdów opiera się na systemie pasów ruchu. Każdy pojazd porusza się po przypisanym `Lane`, a jego pozycja jest wyznaczana na podstawie postępu na danym pasie. System uwzględnia między innymi:

* przyspieszanie i hamowanie,
* zatrzymywanie się na czerwonym świetle,
* zachowanie odstępu od pojazdu poprzedzającego,
* obsługę pojazdów dłuższych, takich jak autobusy i tramwaje,
* zatrzymywanie autobusów na przystankach,
* omijanie oraz ustępowanie pojazdom uprzywilejowanym.

## Sterowanie ruchem

Sygnalizacja świetlna działa w fazach. Długość zielonego światła może być modyfikowana w zależności od liczby pojazdów oczekujących w kolejce. Dzięki temu skrzyżowanie nie działa wyłącznie według stałego cyklu, ale reaguje na aktualne natężenie ruchu.

## Statystyki

Symulacja zbiera podstawowe dane dotyczące ruchu, takie jak:

* liczba pojazdów,
* struktura ruchu według typów pojazdów,
* natężenie ruchu,
* średni czas oczekiwania,
* długość kolejek,
* liczba pojazdów z poszczególnych wlotów.

Po zakończeniu pełnej symulacji mogą zostać wygenerowane wykresy zapisane w katalogu `results`.

## Struktura projektu

```text
core/
    simulation.py

entities/
    moving_entities.py

infrastructure/
    intersection.py
    lane.py
    traffic_light.py
    tram_light.py

systems/
    movement_system.py
    spawn_system.py
    traffic_control_system.py
    stats_system.py

rendering/
    pygame_renderer.py

main.py
```

## Najważniejsze pliki

* `main.py` — uruchomienie symulacji i główna pętla programu.
* `simulation.py` — główny obiekt symulacji, przechowuje encje i systemy.
* `intersection.py` — definicja skrzyżowania, pasów ruchu, świateł i faz.
* `movement_system.py` — logika ruchu pojazdów.
* `spawn_system.py` — generowanie pojazdów.
* `traffic_control_system.py` — sterowanie sygnalizacją świetlną.
* `stats_system.py` — zbieranie i generowanie statystyk.
* `pygame_renderer.py` — wizualizacja symulacji.

## Uruchomienie

Wymagane biblioteki:

```bash
pip install -r requirements.txt
```

Uruchomienie programu:

```bash
python main.py
```

## Sterowanie w symulacji

W interfejsie dostępne są przyciski:

* `PAUSE / PLAY` — zatrzymanie lub wznowienie symulacji,
* `X1`, `X5`, `X10`, `X20` — zmiana prędkości symulacji,
* `X1000` - szybkie generowanie wykresów i danych,
* `RESET` — zresetowanie symulacji,
* `PEAK AM` — ustawienie porannego szczytu komunikacyjnego,
* `PEAK PM` — ustawienie popołudniowego szczytu komunikacyjnego.
