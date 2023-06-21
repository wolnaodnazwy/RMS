import sqlite3

def insert_test_data():
    conn = sqlite3.connect('results/rms.db')
    cursor = conn.cursor()

    # Wstawianie danych testowych do tabeli 'dane'
    cursor.execute('''INSERT INTO dane (
                        Typ_urzadzenia, Numer_seryjny, Lokalizacja,
                        Data_zakupu, Gwarancja
                    ) VALUES
                    ('Laptop', 'ABC123', 'Biuro', '2022-01-01', 'Tak'),
                    ('Smartphone', 'XYZ789', 'Dom', '2022-02-15', 'Nie');''')

    # Wstawianie danych testowych do tabeli 'service'
    cursor.execute('''INSERT INTO service (
                        Numer_seryjny, Data_przegladu, Wynik_przegladu
                    ) VALUES
                    ('ABC123', '2022-03-01', 'Pozytywny'),
                    ('XYZ789', '2022-04-15', 'Negatywny');''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    insert_test_data()