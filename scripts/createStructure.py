from connection import get_database_connection

def check_enum_type_exists(conn, enum_type_name):
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM pg_type WHERE typname = %s)", (enum_type_name,))
    exists = cursor.fetchone()[0]
    cursor.close()
    return exists

def create_database_structure():
    # Uzyskanie połączenia do bazy danych
    conn = get_database_connection()
    cursor = conn.cursor()

    # Sprawdzanie, czy typ enum 'Typ_urzadzenia_enum' już istnieje
    typ_urzadzenia_enum_exists = check_enum_type_exists(conn, 'typ_urzadzenia_enum')

    # Tworzenie typu enum 'Typ_urzadzenia_enum' (jeśli jeszcze nie istnieje)
    if not typ_urzadzenia_enum_exists:
        cursor.execute("CREATE TYPE Typ_urzadzenia_enum AS ENUM ('Laptop', 'Drukarka', 'Smartphone', 'Fax', 'Komputer stacjonarny', 'Tablet', 'Router', 'Skaner', 'Projektor', 'Serwer');")

    # Tworzenie typu enum 'Gwarancja_enum' (jeśli jeszcze nie istnieje)
    gwarancja_enum_exists = check_enum_type_exists(conn, 'gwarancja_enum')
    if not gwarancja_enum_exists:
        cursor.execute("CREATE TYPE Gwarancja_enum AS ENUM ('Tak', 'Nie');")

    # Sprawdzanie, czy tabela 'data' już istnieje
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'data')")
    data_table_exists = cursor.fetchone()[0]

    # Tworzenie tabeli 'data' (jeśli jeszcze nie istnieje)
    if not data_table_exists:
        cursor.execute('''CREATE TABLE data (
                            Typ_urzadzenia Typ_urzadzenia_enum,
                            Numer_seryjny VARCHAR PRIMARY KEY,
                            Lokalizacja VARCHAR,
                            Data_zakupu DATE,
                            Gwarancja Gwarancja_enum
                        );''')

    # Sprawdzanie, czy tabela 'service' już istnieje
    cursor.execute("SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = 'service')")
    service_table_exists = cursor.fetchone()[0]

    # Tworzenie typu enum 'Wynik_przegladu_enum' (jeśli jeszcze nie istnieje)
    wynik_przegladu_enum_exists = check_enum_type_exists(conn, 'wynik_przegladu_enum')
    if not wynik_przegladu_enum_exists:
        cursor.execute("CREATE TYPE Wynik_przegladu_enum AS ENUM ('Pozytywny', 'Negatywny', 'Wstrzymany');")

    # Tworzenie tabeli 'service' (jeśli jeszcze nie istnieje)
    if not service_table_exists:
        cursor.execute('''CREATE TABLE service (
                            Numer_seryjny TEXT REFERENCES data(Numer_seryjny),
                            Data_przegladu DATE,
                            Wynik_przegladu Wynik_przegladu_enum
                        );''')

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_database_structure()
