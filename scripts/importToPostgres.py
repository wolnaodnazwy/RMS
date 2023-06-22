import sqlite3
import psycopg2

def convert_sqlite_to_postgresql(sqlite_path, postgresql_connection_string):
    # Nawiązanie połączenia z bazą danych SQLite
    sqlite_conn = sqlite3.connect(sqlite_path)

    # Uzyskanie schematu bazy danych SQLite
    sqlite_schema = sqlite_conn.iterdump()

    # Nawiązanie połączenia z bazą danych PostgreSQL
    pg_conn = psycopg2.connect(postgresql_connection_string)
    pg_cursor = pg_conn.cursor()

    # Tworzenie tymczasowej tabeli dla każdej tabeli z SQLite
    for line in sqlite_schema:
        try:
            pg_cursor.execute(line)
        except psycopg2.Error as e:
            print(f"Błąd podczas tworzenia tabeli: {e}")

    # Przekształcanie danych dla każdej tabeli z SQLite
    sqlite_cursor = sqlite_conn.cursor()
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        sqlite_cursor.execute(f"SELECT * FROM {table_name};")
        rows = sqlite_cursor.fetchall()

        for row in rows:
            insert_query = f"INSERT INTO {table_name} VALUES {str(row)};"
            try:
                pg_cursor.execute(insert_query)
            except psycopg2.Error as e:
                print(f"Błąd podczas wstawiania danych: {e}")

    # Zatwierdzanie zmian w bazie danych PostgreSQL
    pg_conn.commit()

    # Zamykanie połączeń
    sqlite_cursor.close()
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()

    print("Plik rms.db został pomyślnie zaimportowany do PostgreSQL.")

if __name__ == '__main__':
    sqlite_path = 'results/rms.db'
    postgresql_connection_string = "host='127.0.0.1' port='5432' dbname='student02db' user='student02' password='852BSW529qfdpxGRP'"

    convert_sqlite_to_postgresql(sqlite_path, postgresql_connection_string)