import sqlite3
import pandas as pd

def create_table(conn):
    # Tworzenie tabeli w bazie danych
    conn.execute('''CREATE TABLE IF NOT EXISTS data (
                        Typ_urzadzenia TEXT CHECK(Typ_urzadzenia IN ('Laptop', 'Drukarka', 'Smartphone', 'Fax', 'Komputer stacjonarny', 'Tablet', 'Router', 'Skaner', 'Projektor', 'Serwer')),
                        Numer_seryjny VARCHAR PRIMARY KEY,
                        Lokalizacja TEXT,
                        Data_zakupu TEXT,
                        Gwarancja TEXT CHECK(Gwarancja IN ('Tak', 'Nie'))
                    );''')
    
    # Tworzenie tabeli dla przeglądu
    conn.execute('''CREATE TABLE IF NOT EXISTS service (
                        Numer_seryjny VARCHAR REFERENCES data(Numer_seryjny),
                        Data_przegladu TEXT,
                        Wynik_przegladu TEXT CHECK(Wynik_przegladu IN ('Pozytywny', 'Negatywny', 'Wstrzymany'))
                    );''')

def insert_equipment_data(conn, data):
    # Wstawianie danych o sprzęcie do tabeli w bazie danych
    conn.executemany('''INSERT INTO data (
                        Typ_urzadzenia, Numer_seryjny, Lokalizacja,
                        Data_zakupu, Gwarancja
                    ) VALUES (?, ?, ?, ?, ?);''', data)
    conn.commit()
    
def insert_service_data(conn, data):
    # Wstawianie danych o przeglądzie do tabeli w bazie danych
    conn.executemany('''INSERT INTO service (
                        Numer_seryjny, 
                        Data_przegladu, 
                        Wynik_przegladu
                    ) VALUES (?, ?, ?);''', data)
    conn.commit()

def main():
    # Ładowanie danych z pliku CSV
    equipment_data = pd.read_csv('results/data.csv')
    service_data = pd.read_csv('results/service.csv')
    
    # Nawiązywanie połączenia z bazą danych SQLite
    db_path = "results/rms.db"
    conn = sqlite3.connect(db_path)

    # Ustawienie kodowania dla połączenia SQLite
    conn.text_factory = str
    
    # Tworzenie tabeli w bazie danych
    create_table(conn)

    # Przekształcenie danych o sprzęcie z DataFrame na listę krotek
    equipment_tuples = list(equipment_data.itertuples(index=False, name=None))
    # Wstawianie danych o sprzęcie do tabeli "data"
    insert_equipment_data(conn, equipment_tuples)

    # Przekształcenie danych o przeglądzie z DataFrame na listę krotek
    service_tuples = list(service_data[['Numer seryjny', 'Data przeglądu', 'Wynik przeglądu']].itertuples(index=False, name=None))
    # Wstawianie danych o przeglądzie do tabeli "service"
    insert_service_data(conn, service_tuples)

    # Zamykanie połączenia z bazą danych
    conn.close()

if __name__ == '__main__':
    main()
