import psycopg2

def create_database_structure():
    conn = psycopg2.connect(
        host='127.0.0.1',
        port='5432',
        dbname='student02db',
        user='student02',
        password='852BSW529qfdpxGRP'
    )
    cursor = conn.cursor()

    # Tworzenie tabeli 'dane'
    cursor.execute('''CREATE TABLE IF NOT EXISTS data (
                        Typ_urzadzenia TEXT,
                        Numer_seryjny TEXT,
                        Lokalizacja TEXT,
                        Data_zakupu TEXT,
                        Gwarancja TEXT
                    );''')

    # Tworzenie tabeli 'service'
    cursor.execute('''CREATE TABLE IF NOT EXISTS service (
                        Numer_seryjny TEXT,
                        Data_przegladu TEXT,
                        Wynik_przegladu TEXT
                    );''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database_structure()