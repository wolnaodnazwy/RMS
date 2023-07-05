from connection import get_database_connection

def check_database_structure():
    """
    Sprawdza strukturę bazy danych.

    Returns:
        bool: True, jeśli struktura danych istnieje. False, w przeciwnym razie.
    """
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()
    cursor = conn.cursor()

    # Sprawdzenie istnienia tabeli 'data'
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data');")
    data_table_exists = cursor.fetchone()[0]

    # Sprawdzenie istnienia tabeli 'service'
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'service');")
    service_table_exists = cursor.fetchone()[0]

    conn.close()

    if not data_table_exists or not service_table_exists:
        print("Struktura danych nie istnieje. Proszę najpierw utworzyć strukturę danych.")
        return False

    return True

def insert_test_data():
    """
    Wstawia dane testowe do bazy danych.

    Przed wstawieniem danych sprawdza, czy struktura bazy danych istnieje.
    """
    if not check_database_structure():
        return
    
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()
    cursor = conn.cursor()

    # Wstawianie danych testowych do tabeli 'data'
    cursor.execute('''INSERT INTO data (
                        Typ_urzadzenia, Numer_seryjny, Lokalizacja,
                        Data_zakupu, Gwarancja
                    ) VALUES
                    ('Laptop', 'ABC123', 'Biuro', '2022-01-01', 'Tak'),
                    ...
                    ('Laptop', 'CDE567', 'Dom', '2023-08-05', 'Tak');''')

    # Wstawianie danych testowych do tabeli 'service'
    cursor.execute('''INSERT INTO service (
                        Numer_seryjny, Data_przegladu, Wynik_przegladu
                    ) VALUES
                    ('ABC123', '2022-03-01', 'Pozytywny'),
                    ...
                    ('CDE567', '2023-10-15', 'Wstrzymany');''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_test_data()
