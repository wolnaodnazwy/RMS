from connection import get_database_connection

def check_database_structure():
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
                    ('Smartphone', 'XYZ789', 'Dom', '2022-02-15', 'Nie'),
                    ('Drukarka', 'DEF456', 'Biuro', '2022-03-10', 'Tak'),
                    ('Komputer stacjonarny', 'GHI789', 'Dom', '2022-04-05', 'Nie'),
                    ('Tablet', 'JKL012', 'Biuro', '2022-05-20', 'Tak'),
                    ('Smartphone', 'MNO345', 'Dom', '2022-06-15', 'Tak'),
                    ('Laptop', 'PQR678', 'Biuro', '2022-07-10', 'Nie'),
                    ('Skaner', 'STU901', 'Dom', '2022-08-25', 'Tak'),
                    ('Projektor', 'VWX234', 'Biuro', '2022-09-30', 'Nie'),
                    ('Komputer stacjonarny', 'YZA567', 'Dom', '2022-10-15', 'Tak'),
                    ('Router', 'BCD890', 'Biuro', '2022-11-20', 'Nie'),
                    ('Smartphone', 'EFG123', 'Dom', '2022-12-25', 'Tak'),
                    ('Laptop', 'HIJ456', 'Biuro', '2023-01-30', 'Tak'),
                    ('Drukarka', 'KLM789', 'Dom', '2023-02-05', 'Nie'),
                    ('Smartphone', 'NOP012', 'Biuro', '2023-03-10', 'Tak'),
                    ('Komputer stacjonarny', 'QRS345', 'Dom', '2023-04-15', 'Nie'),
                    ('Skaner', 'TUV678', 'Biuro', '2023-05-20', 'Tak'),
                    ('Tablet', 'WXY901', 'Dom', '2023-06-25', 'Nie'),
                    ('Smartphone', 'ZAB234', 'Biuro', '2023-07-30', 'Tak'),
                    ('Laptop', 'CDE567', 'Dom', '2023-08-05', 'Tak');''')

    # Wstawianie danych testowych do tabeli 'service'
    cursor.execute('''INSERT INTO service (
                        Numer_seryjny, Data_przegladu, Wynik_przegladu
                    ) VALUES
                    ('ABC123', '2022-03-01', 'Pozytywny'),
                    ('XYZ789', '2022-04-15', 'Negatywny'),
                    ('DEF456', '2022-05-20', 'Pozytywny'),
                    ('GHI789', '2022-06-15', 'Negatywny'),
                    ('JKL012', '2022-07-30', 'Wstrzymany'),
                    ('MNO345', '2022-08-25', 'Pozytywny'),
                    ('PQR678', '2022-09-30', 'Negatywny'),
                    ('STU901', '2022-10-15', 'Pozytywny'),
                    ('VWX234', '2022-11-30', 'Negatywny'),
                    ('YZA567', '2022-12-25', 'Wstrzymany'),
                    ('BCD890', '2023-01-30', 'Pozytywny'),
                    ('EFG123', '2023-02-15', 'Negatywny'),
                    ('HIJ456', '2023-03-20', 'Pozytywny'),
                    ('KLM789', '2023-04-25', 'Negatywny'),
                    ('NOP012', '2023-05-30', 'Wstrzymany'),
                    ('QRS345', '2023-06-15', 'Pozytywny'),
                    ('TUV678', '2023-07-30', 'Negatywny'),
                    ('WXY901', '2023-08-05', 'Pozytywny'),
                    ('ZAB234', '2023-09-10', 'Negatywny'),
                    ('CDE567', '2023-10-15', 'Wstrzymany');''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_test_data()
