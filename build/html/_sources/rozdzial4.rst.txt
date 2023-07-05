===============
Rozdział 4
===============

Podsumowanie / raportowanie danych zebranych w bazie danych.
------------------------------ 

Filtrowanie (filter.py)
------------------------------
 Po nawiązaniu połączenia z bazą danych, użytkownik może wybrać tabelę, następnie kolumnę i wartość filtru. Po wykonaniu filtracji, wyświetlane są wyniki lub informacja o ich braku. Użytkownik ma również opcję generowania raportu w formacie CSV na podstawie przefiltrowanych danych.

Kod składa się z funkcji, które realizują konkretne operacje na bazie danych, takie jak sprawdzanie istnienia tabeli, pobieranie dostępnych tabel, pobieranie nazw kolumn, pobieranie wartości z kolumny oraz filtrowanie danych. Skrypt również importuje moduły zawierające funkcje do nawiązywania połączenia z bazą danych i generowania raportów.

Główna pętla programu pozwala użytkownikowi na interaktywne wybieranie tabeli, kolumny i wartości filtru. Po wybraniu opcji, wywoływane są odpowiednie funkcje do pobierania danych i wyświetlania wyników lub generowania raportu.

Statystyka i wykresy (summary.py)
------------------------------
1. Otwarcie pliku JSON z danymi połączenia z bazą danych.
2. Tworzenie URI połączenia na podstawie danych z pliku JSON.
3. Pobieranie danych z tabeli 'data' i 'service' z wykorzystaniem zapytań SQL i silnika SQLAlchemy.
4. Obliczanie różnych podsumowań i udziałów procentowych na podstawie otrzymanych danych.
5. Generowanie wykresu słupkowego na podstawie danych o typach urządzeń.
6. Zapisywanie podsumowania i wykresu do pliku CSV.
7. Wyświetlanie podsumowania na konsoli.
8. Tworzenie katalogu "results" dla zapisanych wyników.
9. Zapisywanie zakodowanego obrazu wykresu jako załącznika w pliku CSV.
10. Wywołanie funkcji generującej raport podsumowujący.

Generowanie raportu (raportGenerator.py)
------------------------------
Importowanie modułów:
csv: Moduł do obsługi plików CSV.
os: Moduł do interakcji z systemem operacyjnym.
from connection import get_database_connection: Importuje funkcję get_database_connection z modułu connection, która służy do nawiązywania połączenia z bazą danych.
generate_report(table_name, column_name, filter_value=None, filename='report.csv'): Funkcja generuje raport na podstawie danych z tabeli w bazie danych. Przyjmuje argumenty: table_name - nazwa tabeli, column_name - nazwa kolumny do filtrowania, filter_value - wartość filtru (opcjonalna, domyślnie None), filename - nazwa pliku raportu (opcjonalna, domyślnie 'report.csv').

a. Funkcja nawiązuje połączenie z bazą danych.

b. Sprawdza istnienie tabeli i kolumny.

c. Wykonuje filtrowanie danych na podstawie wartości w kolumnie.

d. Jeśli są wyniki filtrowania, tworzy plik raportu w formacie CSV w katalogu "results" (jeśli nie istnieje, tworzy go). Plik zawiera nazwy kolumn i przefiltrowane wiersze.

e. Wyświetla informację o utworzeniu i zapisaniu raportu, lub informację o braku wyników filtrowania.

f. Zamyka kursor i połączenie z bazą danych.
