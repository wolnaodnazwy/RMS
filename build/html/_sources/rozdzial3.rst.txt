===============
Rozdział 3
===============

Stworzona aplikacja umożliwia zarządzanie bazą danych, która zajmuje się obsługą serwisową dla wskazanego budynku. Baza zawiera dane odnośnie dostepnego sprzętu oraz to gdzie się znajduje. Można nazwać ją jako inwentaryzację sprzętową. Numer seryjny sprzętu jest kluczem głównym dla tej bazy.

Opis działania konwertowania z SQLite do PostgreSQL
------------------------------
1.Wczytuje dane o sprzęcie i przeglądach z plików CSV przy użyciu biblioteki pandas.
2.Nawiązuje połączenie z bazą danych PostgreSQL poprzez wywołanie funkcji get_database_connection.
3.Wywołuje funkcję create_table, aby utworzyć wymagane tabele w bazie danych.
4.Przekształca dane o sprzęcie i przeglądach z obiektów DataFrame na listy krotek.
5.Wywołuje funkcję insert_equipment_data, aby wstawić dane o sprzęcie do tabeli "data" w bazie danych.
6.Wywołuje funkcję insert_service_data, aby wstawić dane o przeglądach do tabeli "service" w bazie danych.
7.Zatwierdza zmiany w bazie danych przy użyciu metody commit.
8.Zamyka połączenie z bazą danych przez wywołanie metod close na obiektach kursora i połączenia.
9.Na końcu, sprawdzane jest, czy skrypt jest uruchomiony jako plik główny, a jeśli tak, to wywoływana jest funkcja main w celu wykonania programu.

Kod z omówieniem
------------------------------
import pandas as pd
import simplejson
from connection import get_database_connection


# Sprawdzenie, czy typy enum już istnieją

def create_table(cursor):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = 'typ_urzadzenia_enum')")
    typ_urzadzenia_exists = cursor.fetchone()[0]
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = 'gwarancja_enum')")
    gwarancja_exists = cursor.fetchone()[0]
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = 'wynik_przegladu_enum')")
    wynik_przegladu_exists = cursor.fetchone()[0]

# Tworzenie typu enum 'Typ_urzadzenia', jeśli nie istnieje

    if not typ_urzadzenia_exists:
        cursor.execute("CREATE TYPE Typ_urzadzenia_enum AS ENUM ('Laptop', 'Drukarka', 'Smartphone', 'Fax', 'Komputer stacjonarny', 'Tablet', 'Router', 'Skaner', 'Projektor', 'Serwer');")

# Tworzenie typu enum 'Gwarancja', jeśli nie istnieje

    if not gwarancja_exists:
        cursor.execute("CREATE TYPE Gwarancja_enum AS ENUM ('Tak', 'Nie');")

# Tworzenie tabeli 'data', jeśli nie istnieje

    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        Typ_urzadzenia Typ_urzadzenia_enum,
                        Numer_seryjny VARCHAR PRIMARY KEY,
                        Lokalizacja VARCHAR,
                        Data_zakupu DATE,
                        Gwarancja Gwarancja_enum
                    );''')

# Tworzenie typu enum 'Wynik_przegladu', jeśli nie istnieje

    if not wynik_przegladu_exists:
        cursor.execute("CREATE TYPE Wynik_przegladu_enum AS ENUM ('Pozytywny', 'Negatywny', 'Wstrzymany');")

# Tworzenie tabeli 'service', jeśli nie istnieje

    cursor.execute('''CREATE TABLE IF NOT EXISTS service (
                        Numer_seryjny TEXT REFERENCES data(Numer_seryjny),
                        Data_przegladu DATE,
                        Wynik_przegladu Wynik_przegladu_enum
                    );''')

# Wstawianie danych o sprzęcie do tabeli w bazie danych

def insert_equipment_data(cursor, data):
    cursor.executemany('''INSERT INTO data (
                        Typ_urzadzenia, Numer_seryjny, Lokalizacja,
                        Data_zakupu, Gwarancja
                    ) VALUES (%s, %s, %s, %s, %s);''', data)

# Wstawianie danych o przeglądzie do tabeli w bazie danych

def insert_service_data(cursor, data):
    cursor.executemany('''INSERT INTO service (
                        Numer_seryjny, 
                        Data_przegladu, 
                        Wynik_przegladu
                    ) VALUES (%s, %s, %s);''', data)

def main():
# Ładowanie danych z pliku CSV

    equipment_data = pd.read_csv('results/data.csv')
    service_data = pd.read_csv('results/service.csv')

# Nawiązywanie połączenia z bazą danych PostgreSQL

    conn = get_database_connection()
    cursor = conn.cursor()

# Tworzenie tabeli w bazie danych PostgreSQL

    create_table(cursor)
    conn.commit()

# Przekształcenie danych o sprzęcie z DataFrame na listę krotek

    equipment_tuples = [tuple(row) for row in equipment_data.itertuples(index=False)]
    # Wstawianie danych o sprzęcie do tabeli "data"
    insert_equipment_data(cursor, equipment_tuples)

# Przekształcenie danych o przeglądzie z DataFrame na listę krotek

    service_tuples = [tuple(row) for row in service_data[['Numer seryjny', 'Data przeglądu', 'Wynik przeglądu']].itertuples(index=False)]
# Wstawianie danych o przeglądzie do tabeli "service"

    insert_service_data(cursor, service_tuples)

# Zatwierdzanie zmian w bazie danych PostgreSQL

    conn.commit()

# Zamykanie połączenia

    cursor.close()
    conn.close()

if __name__ == '__main__':
    main()
