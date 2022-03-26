# Skrypt do pobierania demek z pukawki

## Parametry
* max_weight - maksymalna waga demek w GB; Jeżeli waga pobieranych demek z danego dnia przekracza łączny limit, to nie pobiera więcej demek.
* keep_for_days - przez ile dni przechowywać demka, tzn. demka starsze niż X dni są usuwane przed rozpoczęciem pobierania nowych.
* servers_urls - słownik o formacie: "nazwa folderu: link do demek"


## Opis
Prosty skrypt do pobierania demek z pukawki. <br />
Można wrzucić na własny serwer www i dodać do CRON'a, żeby przechowywać demka np. z 15 dni zamiast z 7 jak to robi pukawka.
